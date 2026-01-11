# Projet Big Data : Prédiction de la Consommation Électrique

**Université Paris 8 - Master 2 Big Data**
**Auteurs :** ARNAOUT Richard, ATMACA Serkan

---

## 📋 Description du projet

Ce projet vise à prédire la consommation énergétique nationale (en Mégawatts) en fonction de données météorologiques et temporelles.

Il met en œuvre une architecture **Big Data** hybride et modulaire :
1.  **ETL Distribué (PySpark) :** Nettoyage, agrégation et jointure des données massives (fichiers CSV bruts).
2.  **Machine Learning (Scikit-Learn) :** Comparaison de modèles (Régression Linéaire vs Random Forest) pour la prédiction finale.

---

## 📂 Organisation du Projet

Le projet respecte les standards industriels **Cookiecutter Data Science**.

```text
projet_energie_bigdata
├── LICENSE
├── README.md              <- Le fichier que vous lisez actuellement
├── requirements.txt       <- Les dépendances pour reproduire l'environnement
├── setup.py               <- Rend le projet installable (pip install -e .)
│
├── data
│   ├── processed          <- Données finales nettoyées (Format Parquet)
│   └── raw                <- Données brutes originales (CSV Kaggle)
│
├── reports                <- Analyses générées
│   └── figures            <- Graphiques de résultats (Courbes de prédiction)
│
└── src                    <- Code source du projet
    ├── __init__.py        <- Rend le dossier src importable comme un module
    │
    ├── data               <- Scripts d'ETL (Extraction & Nettoyage)
    │   └── make_dataset.py
    │
    └── models             <- Scripts d'entraînement et de prédiction
        ├── train_linear_regression.py
        └── train_random_forest.py
```


## 🚀 Installation et configuration

Pour garantir le bon fonctionnement du projet (notamment **PySpark** et **Scikit-Learn**), veuillez respecter les prérequis ci-dessous.

### 1️⃣ Prérequis système

- **Python 3.10** (minimum requis)
- **Java JDK 8 ou 11** (indispensable pour Apache Spark)
- Système d’exploitation : **Windows**, **macOS** ou **Linux**

---

### 2️⃣ Création de l’environnement virtuel (recommandé)

Il est fortement conseillé d’isoler le projet dans un environnement virtuel afin d’éviter les conflits de versions.

Depuis la racine du projet :

```bash
# Création de l'environnement virtuel
python -m venv .venv
```

Activation de l’environnement :
```bash
# Windows
.\.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### 3️⃣ Installation des dépendances
Une fois l’environnement virtuel activé, installez les dépendances nécessaires :
```bash
pip install -r ./src/requirements.txt
```

### ▶️ Exécution du projet
L’exécution du projet se déroule en deux étapes principales :

1.  **Préparation des données (ETL avec PySpark) :**
2.  **Entraînement et évaluation des modèles de Machine Learning :**

#### 🧹 Étape 1 : Préparation des données (ETL PySpark)

Ce script :
- **Lance Apache Spark** 
- **Nettoie les fichiers CSV bruts** 
- **Gère les valeurs manquantes** 
- **Produit un dataset final optimisé au format Parquet** 

```bash
python src/data/make_dataset.py
```

#### 🤖 Étape 2 : Entraînement et comparaison des modèles

Les modèles peuvent être exécutés indépendamment.

🔹 Modèle 1 : Régression Linéaire (baseline)

```bash
python src/models/train_linear_regression.py
```

#### 📊 Résultats :

RMSE ≈ 3808.01 MW

Génération du graphique :

reports/figures/resultat_lineaire.png (courbe verte)

🔹 Modèle 2 : Random Forest (modèle retenu)
```bash
python src/models/train_random_forest.py
```
📊 Résultats :

RMSE ≈ 2670 MW

Génération du graphique :

reports/figures/resultat_random_forest.png (courbe rouge)

➡️ Ce modèle est retenu comme solution finale pour la prédiction de la consommation électrique.


