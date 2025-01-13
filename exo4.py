import pandas as pd

# Charger le fichier CSV dans un DataFrame (remplacez 'popular_tracks_with_genres_and_play_counts.csv' par votre fichier)
df = pd.read_csv('cleaned_popular_tracks.csv')

# Filtrer les données valides
df = df[df['Popularity'].notnull()]  # S'assurer que "Popularity" n'est pas vide

# 1. Filtrer les chansons avec une popularité supérieure à la moyenne globale
mean_popularity = df['Popularity'].mean()
high_popularity_songs = df[df['Popularity'] > mean_popularity]
print(f"Popularité moyenne globale : {mean_popularity:.2f}")
print(f"Nombre de chansons avec une popularité supérieure à la moyenne : {len(high_popularity_songs)}")

# 2. Classer les chansons par "Popularité" décroissante
sorted_songs = high_popularity_songs.sort_values(by='Popularity', ascending=False)

# 3. Afficher les 10 meilleures chansons et leurs artistes
top_10_songs = sorted_songs[['Track Name', 'Artist Name', 'Popularity']].head(10)
print("\nLes 10 meilleures chansons avec leur artiste :")
print(top_10_songs.to_string(index=False))
