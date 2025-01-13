import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Load the dataset
# Replace 'spotify_data.csv' with the actual path to your CSV file.
df = pd.read_csv('popular_tracks_with_genres_and_play_counts.csv')

# 1. Fill missing genres and clean up
df['Genres'] = df['Genres'].fillna('Unknown')  # Fill missing genres with "Unknown"

# 2. Count the number of songs per genre
# Split genres by commas and count the occurrences
genre_counts = df['Genres'].str.split(',').explode().value_counts()

# Display the number of songs per genre
print("Number of songs per genre:")
print(genre_counts)

# 3. Identify the most represented genre
most_represented_genre = genre_counts.idxmax()
most_represented_count = genre_counts.max()
print(f"\nThe most represented genre is: {most_represented_genre} with {most_represented_count} songs.")

# 4. Create a bar plot to show the distribution of genres
plt.figure(figsize=(12, 6))
genre_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribution of Music Genres', fontsize=16)
plt.xlabel('Genres', fontsize=12)
plt.ylabel('Number of Songs', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Export the cleaned dataset to a new CSV file
df_cleaned_path = 'cleaned_popular_tracks.csv'
df.to_csv(df_cleaned_path, index=False)

print(f"\nThe cleaned dataset has been saved to {df_cleaned_path}.")
