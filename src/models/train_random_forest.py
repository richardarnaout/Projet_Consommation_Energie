# Fichier : src/models/train_random_forest.py
import os
import pandas as pd
import matplotlib.pyplot as plt

from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.sql.functions import mean

def main():
    # 1. Init Spark
    spark = SparkSession.builder \
        .appName("ProjetEnergieRF") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()

    print("-" * 50)
    print(">>> Démarrage RANDOM FOREST (PySpark MLlib)...")

    # 2. Chemins
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(os.path.dirname(current_dir))
    path_input = os.path.join(project_dir, "data", "processed", "donnees_finales.parquet")
    path_fig = os.path.join(project_dir, "reports", "figures", "resultat_random_forest.png")

    # 3. Chargement
    try:
        pdf = pd.read_parquet(path_input)
        if "dt_iso" in pdf.columns: pdf = pdf.drop(columns=["dt_iso"])
        df = spark.createDataFrame(pdf)
    except Exception as e:
        print(e); return

    # 4. Features
    assembler = VectorAssembler(inputCols=["temperature_moyenne", "humidite_moyenne", "heure", "mois", "jour_semaine"], outputCol="features")
    data_ml = assembler.transform(df).select("features", "consommation")

    # 5. Split
    train_data, test_data = data_ml.randomSplit([0.8, 0.2], seed=42)

    # 6. Entraînement Random Forest
    print(">>> Entraînement en cours...")
    rf = RandomForestRegressor(featuresCol="features", labelCol="consommation", numTrees=50, maxDepth=8, seed=42)
    model = rf.fit(train_data)

    # 7. Évaluation
    predictions = model.transform(test_data)
    evaluator = RegressionEvaluator(labelCol="consommation", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)
    moyenne_conso = test_data.select(mean("consommation")).first()[0]
    error_pct = (rmse / moyenne_conso) * 100

    print(f"\n>>> RESULTAT RANDOM FOREST : RMSE={rmse:.2f} MW | Erreur={error_pct:.2f} %\n")

    # 8. Graphique
    preds_pd = predictions.select("consommation", "prediction").limit(200).toPandas()
    plt.figure(figsize=(14, 6))
    plt.plot(preds_pd["consommation"], label="Réel", color="blue")
    plt.plot(preds_pd["prediction"], label="Random Forest", color="red", linestyle="--")
    plt.title(f"Random Forest (PySpark) - Erreur: {error_pct:.2f}%")
    plt.legend()
    plt.grid(True)
    os.makedirs(os.path.dirname(path_fig), exist_ok=True)
    plt.savefig(path_fig)
    print(f">>> Graphique sauvegardé : {path_fig}")

if __name__ == '__main__':
    main()