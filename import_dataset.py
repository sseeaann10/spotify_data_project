import requests
import pandas as pd
import time

# Spotify API credentials
SPOTIFY_CLIENT_ID = "7ecd2654eea5436eaf7c28b01c01164c"
SPOTIFY_CLIENT_SECRET = "0c0f30323f264288acc5e370c2b024f9"


# Get Spotify access token
def get_spotify_access_token(client_id, client_secret):
    url = "https://accounts.spotify.com/api/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
    response.raise_for_status()
    return response.json()["access_token"]

# Fetch playlists by year
def fetch_playlists_by_year(year, access_token):
    url = "https://api.spotify.com/v1/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"q": f"Top 100 {year}", "type": "playlist", "limit": 1}
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    playlists = response.json().get("playlists", {}).get("items", [])
    return playlists[0].get("id") if playlists else None

# Fetch tracks from a playlist
def fetch_tracks_from_playlist(playlist_id, access_token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {"Authorization": f"Bearer {access_token}"}
    tracks = []
    while url:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        items = data.get("items", [])
        for item in items:
            track = item.get("track", {})
            if track:
                tracks.append({
                    "name": track.get("name"),
                    "artist": track.get("artists", [{}])[0].get("name"),
                    "artist_id": track.get("artists", [{}])[0].get("id"),
                    "id": track.get("id"),
                    "url": track.get("external_urls", {}).get("spotify")
                })
        url = data.get("next")
        time.sleep(1)  # Add sleep to prevent rate limiting
    return tracks

# Fetch track metadata via Spotify API
def fetch_track_details_from_api(track_id, access_token):
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    track_data = response.json()
    return {
        "Track Name": track_data["name"],
        "Artist Name": track_data["artists"][0]["name"],
        "Artist ID": track_data["artists"][0]["id"],
        "Album Name": track_data["album"]["name"],
        "Release Date": track_data["album"]["release_date"],
        "Popularity": track_data["popularity"],
    }

# Fetch artist genres via Spotify API
def fetch_artist_genres(artist_id, access_token):
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    artist_data = response.json()
    return artist_data.get("genres", [])

def main():
    spotify_access_token = get_spotify_access_token(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    all_tracks = []

    for year in range(1990, 2024):
        print(f"Fetching playlist for {year}...")
        playlist_id = fetch_playlists_by_year(year, spotify_access_token)
        if not playlist_id:
            print(f"No playlist found for {year}.")
            continue

        print(f"Fetching tracks for playlist {playlist_id}...")
        tracks = fetch_tracks_from_playlist(playlist_id, spotify_access_token)
        print(f"Found {len(tracks)} tracks for {year}.")

        for track in tracks:
            track_id = track["id"]
            artist_id = track["artist_id"]

            try:
                print(f"Fetching metadata for track ID: {track_id}...")
                metadata = fetch_track_details_from_api(track_id, spotify_access_token)

                print(f"Fetching artist genres for artist ID: {artist_id}...")
                genres = fetch_artist_genres(artist_id, spotify_access_token)

                metadata["Genres"] = ", ".join(genres) if genres else "N/A"
                all_tracks.append(metadata)

                time.sleep(1)  # Prevent rate-limiting
            except Exception as e:
                print(f"Error processing track ID {track_id}: {e}")

    print(f"Total tracks fetched: {len(all_tracks)}")

    # Save to CSV
    df = pd.DataFrame(all_tracks)
    output_file = "popular_tracks_with_genres_and_popularity.csv"
    df.to_csv(output_file, index=False)
    print(f"Data saved to {output_file}")

if __name__ == "__main__":
    main()
