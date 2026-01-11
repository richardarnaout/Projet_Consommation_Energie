# Fichier : src/data/make_dataset.py
import os
import sys
import pandas as pd  # On importe pandas explicitement
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, hour, month, dayofweek, avg

def main():
    # 1. Initialisation de Spark
    spark = SparkSession.builder \
        .appName("ProjetEnergieETL") \
        .config("spark.driver.memory", "4g") \
        .getOrCreate()
    
    print("-" * 50)
    print(">>> Spark Session lancée.")

    # 2. Chemins
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(current_dir))
    
    path_energy = os.path.join(project_dir, "data", "raw", "energy_dataset.csv")
    path_weather = os.path.join(project_dir, "data", "raw", "weather_features.csv")
    path_output = os.path.join(project_dir, "data", "processed", "donnees_finales.parquet")

    # 3. Chargement
    print(f">>> Chargement : {path_energy}")
    try:
        df_energy = spark.read.csv(path_energy, header=True, inferSchema=True)
        df_weather = spark.read.csv(path_weather, header=True, inferSchema=True)
    except Exception as e:
        print("ERREUR : Fichiers introuvables.")
        print(e)
        return

    # 4. Nettoyage & Renommage
    print(">>> Nettoyage...")
    
    if "time" in df_energy.columns:
        print(">>> Renommage 'time' -> 'dt_iso' (Energie)")
        df_energy = df_energy.withColumnRenamed("time", "dt_iso")
        
    if "time" in df_weather.columns:
        df_weather = df_weather.withColumnRenamed("time", "dt_iso")

    df_energy = df_energy.dropna(subset=["total load actual"])
    df_energy = df_energy.withColumnRenamed("total load actual", "consommation") \
                         .select("dt_iso", "consommation")

    df_weather_agg = df_weather.groupBy("dt_iso").agg(
        avg("temp").alias("temperature_moyenne"),
        avg("humidity").alias("humidite_moyenne")
    )

    # 5. Jointure
    print(">>> Jointure...")
    df_final = df_energy.join(df_weather_agg, on="dt_iso", how="inner")

    # 6. Feature Engineering
    df_final = df_final.withColumn("dt_iso", to_timestamp("dt_iso")) \
                       .withColumn("heure", hour("dt_iso")) \
                       .withColumn("mois", month("dt_iso")) \
                       .withColumn("jour_semaine", dayofweek("dt_iso"))

    # 7. Sauvegarde
    print(f">>> Tentative de sauvegarde vers : {path_output}")
    
    try:
        print(">>> Conversion en Pandas (Méthode robuste)...")
        # On récupère les données sous forme de liste Python 
        data_collected = df_final.collect()
        

        df_pandas = pd.DataFrame(data_collected, columns=df_final.columns)
        

        os.makedirs(os.path.dirname(path_output), exist_ok=True)
        

        df_pandas.to_parquet(path_output, index=False)
        print(">>> SUCCÈS ! Fichier sauvegardé via Pandas.")
        
    except Exception as e:
        print(">>> ERREUR FATALE (Même le plan B a échoué).")
        print(e)

    print("-" * 50)
    print(">>> TERMINÉ.")

if __name__ == '__main__':
    main()