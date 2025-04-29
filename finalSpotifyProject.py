import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Spotify API credentials (replace with your own credentials)
SPOTIPY_CLIENT_ID = ("1b5d2950233141f786e6197424829441")
SPOTIPY_CLIENT_SECRET = ("cdbdb2e80a5a4c3ca5fbd78313bf5f91")

# AUTHENTICATION
# Function to create and return a Spotify client using the Spotipy library
def create_spotify_client():
    client_id = ("1b5d2950233141f786e6197424829441")
    client_secret = ("cdbdb2e80a5a4c3ca5fbd78313bf5f91")
    if not client_id or not client_secret:
        raise ValueError("Missing credentials.")  # Raise an error if credentials are missing
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)  # Return an authenticated Spotify client

# SEARCH
# Function to search for tracks based on a query
def search_track(sp, query, limit=5):
    results = sp.search(q=query, limit=limit, type='track')  # Perform a search query
    return [{
        'id': item['id'],  # Track ID
        'name': item['name'],  # Track name
        'artist': item['artists'][0]['name'],  # Artist name
        'url': item['external_urls']['spotify']  # Spotify URL for the track
    } for item in results['tracks']['items']]

# RECOMMENDATIONS
# Function to get track recommendations based on a seed track ID
def get_recommendations(sp, seed_track_id, limit=5):
    recs = sp.recommendations(seed_tracks=[seed_track_id], limit=limit)  # Fetch recommendations
    return [{
        'name': track['name'],  # Recommended track name
        'artist': track['artists'][0]['name'],  # Artist name
        'url': track['external_urls']['spotify']  # Spotify URL for the recommended track
    } for track in recs['tracks']]

# TOP TRACKS
# Function to fetch the top tracks of an artist
def get_top_tracks(sp, artist_id, country="US", limit=5):
    try:
        results = sp.artist_top_tracks(artist_id, country=country)  # Fetch top tracks
        return [{
            'id': track['id'],  # Track ID
            'name': track['name'],  # Track name
            'artist': track['artists'][0]['name'],  # Artist name
            'url': track['external_urls']['spotify']  # Spotify URL for the track
        } for track in results['tracks'][:limit]]
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")  # Handle Spotify API errors
        return []
    except Exception as e:
        print(f"Error fetching top tracks: {e}")  # Handle other errors
        return []

# RELATED ARTISTS
# Function to fetch related artists for a given artist
def get_related_artists(sp, artist_id):
    try:
        results = sp.artist_related_artists(artist_id)  # Fetch related artists
        return [{
            'name': artist['name'],  # Related artist name
            'url': artist['external_urls']['spotify']  # Spotify URL for the related artist
        } for artist in results['artists']]
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")  # Handle Spotify API errors
        return []
    except Exception as e:
        print(f"Error fetching related artists: {e}")  # Handle other errors
        return []

# AUDIO FEATURES
# Function to fetch audio features for a specific track
def get_audio_features(sp, track_id):
    try:
        features = sp.audio_features([track_id])[0]  # Fetch audio features
        if not features:
            raise ValueError("No audio features found for the track.")  # Handle missing features
        return {
            'danceability': features['danceability'],  # Danceability score
            'energy': features['energy'],  # Energy score
            'tempo': features['tempo'],  # Tempo in beats per minute
            'valence': features['valence']  # Valence score (positivity)
        }
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")  # Handle Spotify API errors
        return None
    except Exception as e:
        print(f"Error fetching audio features: {e}")  # Handle other errors
        return None

# MAIN FUNCTION
# Entry point for the application
def main():
    print("🎧 Welcome to the Music Discovery App")

    try:
        sp = create_spotify_client()  # Create a Spotify client
    except Exception as e:
        print("Auth error:", e)  # Handle authentication errors
        return

    # Prompt the user to search for an artist
    query = input("\n Search for an artist: ")
    results = sp.search(q=query, type='artist', limit=1)  # Search for the artist
    if not results['artists']['items']:
        print("No artist found.")  # Handle case where no artist is found
        return

    artist = results['artists']['items'][0]  # Get the first artist from the results
    print(f"\n Found artist: {artist['name']}")

    # Fetch and display the number of followers the artist has on Spotify
    total_tracks = artist['followers']['total']  # Approximation using followers
    print(f"\n {artist['name']} has approximately {total_tracks} followers on Spotify.")

    # Fetch top tracks for the artist
    top_tracks = get_top_tracks(sp, artist['id'])
    if not top_tracks:
        print("No top tracks found for this artist.")  # Handle case where no top tracks are found
        return

    print("\n Top Tracks:")
    for idx, track in enumerate(top_tracks, start=1):
        print(f"{idx}. {track['name']} by {track['artist']} - {track['url']}")

    # Allow the user to select a track to view its audio features
    try:
        track_choice = int(input("\n Select a track number to view its audio features (1-5): "))
        if track_choice < 1 or track_choice > len(top_tracks):
            print("Invalid choice. Exiting.")  # Handle invalid input
            return
        selected_track = top_tracks[track_choice - 1]
        print(f"\n Selected Track: {selected_track['name']} by {selected_track['artist']}")

        # Fetch and display audio features for the selected track
        features = get_audio_features(sp, selected_track['id'])
        if not features:
            print("Unable to fetch audio features for the selected track.")  # Handle missing features
            return

        print("\n Audio Features:")
        for k, v in features.items():
            print(f"{k.title()}: {v}")  # Display audio features
    except ValueError:
        print("Invalid input. Please enter a number.")  # Handle non-numeric input

    # Fetch and display a related artist
    related_artists = get_related_artists(sp, artist['id'])
    if related_artists:
        related_artist = related_artists[0]  # Pick the first related artist
        print(f"\n You might also like: {related_artist['name']} - {related_artist['url']}")
    else:
        print("\n No similar artists found.")  # Handle case where no related artists are found

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
