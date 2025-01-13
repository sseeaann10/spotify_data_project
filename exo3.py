import pandas as pd
import matplotlib.pyplot as plt

# Charger le fichier CSV dans un DataFrame (remplacez 'spotify_data.csv' par votre fichier)
df = pd.read_csv('cleaned_popular_tracks.csv')

# Convertir la colonne "Release Date" en format datetime pour extraire l'année
df['Release Date'] = pd.to_datetime(df['Release Date'], errors='coerce')
df['Year'] = df['Release Date'].dt.year

# Filtrer les données valides (Popularité non nulle et année non manquante)
df = df[df['Popularity'].notnull() & df['Year'].notnull()]

# 1. Grouper par année et calculer la moyenne de popularité
avg_popularity_by_year = df.groupby('Year')['Popularity'].mean()
print("Moyenne de popularité par année :")
print(avg_popularity_by_year)

# 2. Créer une courbe illustrant cette tendance temporelle
plt.figure(figsize=(12, 6))
avg_popularity_by_year.plot(kind='line', marker='o', color='skyblue', linestyle='-')
plt.title("Tendance de la popularité moyenne par année", fontsize=16)
plt.xlabel("Année", fontsize=12)
plt.ylabel("Popularité moyenne", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.show()

# 3. Interprétation des résultats
print("\nLes années les plus marquantes (avec la popularité moyenne maximale et minimale) :")
most_popular_year = avg_popularity_by_year.idxmax()
least_popular_year = avg_popularity_by_year.idxmin()
print(f"- Année la plus marquante (popularité max) : {most_popular_year} avec une popularité moyenne de {avg_popularity_by_year[most_popular_year]:.2f}")
print(f"- Année la moins populaire (popularité min) : {least_popular_year} avec une popularité moyenne de {avg_popularity_by_year[least_popular_year]:.2f}")
