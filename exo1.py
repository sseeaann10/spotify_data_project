# Step 1: Import the necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Step 2: Load the dataset
# Replace 'spotify_data.csv' with the actual path to your CSV file.
df = pd.read_csv('popular_tracks_with_genres_and_play_counts.csv')

# Display the first 5 rows of the dataset
print("First 5 rows of the dataset:")
print(df.head())

# Step 3: Identify missing or inconsistent values
# Check for missing values
print("\nMissing values in each column:")
print(df.isnull().sum())

# Justify the treatment
# - Missing values in "Play Count" (or others): Could be replaced with 0 or estimated based on popularity.
# - Verify inconsistencies in the "Release Date" column if it's not uniform.

# Step 4: Display descriptive statistics
print("\nDescriptive statistics for relevant columns:")
print(df.describe())

# You can calculate specific statistics like mean, median, min, max for numeric columns (like Popularity):
print("\nStatistics for 'Popularity':")
print(f"Mean: {df['Popularity'].mean()}")
print(f"Median: {df['Popularity'].median()}")
print(f"Min: {df['Popularity'].min()}")
print(f"Max: {df['Popularity'].max()}")