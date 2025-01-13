import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

# Charger le jeu de données
data = pd.read_csv("cleaned_popular_tracks.csv")

# Préparer les données
# Assurer que nous avons les colonnes requises
data = data[["Genres", "Release Date", "Popularity"]].dropna(subset=["Genres", "Popularity"])

# Extraire l'année de la date de sortie et gérer les années manquantes
data["Year"] = pd.to_datetime(data["Release Date"], errors="coerce").dt.year
data["Year"].fillna(data["Year"].mode()[0], inplace=True)  # Remplir les années manquantes avec l'année la plus fréquente

# Définir les caractéristiques et la cible
X = data[["Genres", "Year"]]  # Caractéristiques : Genres et Année
y = data["Popularity"]  # Cible : Popularité

# Définir le pipeline de prétraitement
preprocessor = ColumnTransformer(
    transformers=[
        ('genre', OneHotEncoder(handle_unknown='ignore'), ['Genres']),  # Encodage des genres
        ('year', StandardScaler(), ['Year'])  # Mise à l'échelle de l'année
    ])

# Créer un pipeline avec prétraitement et modèle
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))  # Modèle de régression RandomForest
])

# Diviser les données en ensembles d'entraînement (80%) et de test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner le modèle
pipeline.fit(X_train, y_train)

# Prédire sur l'ensemble de test
y_pred = pipeline.predict(X_test)

# Calculer le R² et l'erreur absolue moyenne (MAE)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

# Afficher les résultats
print("Évaluation du modèle :")
print(f"Score R² : {r2:.2f}")
print(f"Erreur absolue moyenne (MAE) : {mae:.2f}")

# Sauvegarder les résultats de l'évaluation du modèle dans un fichier README
with open("README_model_evaluation.txt", "w") as file:
    file.write("Évaluation du modèle :\n")
    file.write(f"Score R² : {r2:.2f}\n")
    file.write(f"Erreur absolue moyenne (MAE) : {mae:.2f}\n")
    
    # Analyser si le modèle est satisfaisant
    if r2 > 0.5:
        file.write("\nLe modèle est raisonnablement satisfaisant, capturant plus de 50% de la variance de la popularité.")
    else:
        file.write("\nLe modèle n'est pas satisfaisant, car le score R² indique qu'il ne capture pas assez de variance dans la popularité.")
    
    file.write("\nUne amélioration pourrait consister à inclure davantage de caractéristiques (par exemple, le nombre de lectures, des métriques sur l'artiste, etc.).")
    
    # Suggérer une amélioration du modèle
    if r2 < 0.3:
        file.write("\nEnvisagez d'explorer des modèles plus sophistiqués comme XGBoost, ou d'ajouter des caractéristiques supplémentaires telles que la durée des morceaux, les caractéristiques liées à l'artiste, etc.")
