import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIPY_CLIENT_ID=("1b5d2950233141f786e6197424829441")
SPOTIPY_CLIENT_SECRET=("cdbdb2e80a5a4c3ca5fbd78313bf5f91")

# AUTHENTICATION
def create_spotify_client():
    client_id=("1b5d2950233141f786e6197424829441")
    client_secret=("cdbdb2e80a5a4c3ca5fbd78313bf5f91")
    if not client_id or not client_secret:
        raise ValueError("Missing credentials.")
    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    return spotipy.Spotify(auth_manager=auth_manager)

#  SEARCH
def search_track(sp, query, limit=5):
    results = sp.search(q=query, limit=limit, type='track')
    return [{
        'id': item['id'],
        'name': item['name'],
        'artist': item['artists'][0]['name'],
        'url': item['external_urls']['spotify']
    } for item in results['tracks']['items']]

#  RECOMMENDATIONS
def get_recommendations(sp, seed_track_id, limit=5):
    recs = sp.recommendations(seed_tracks=[seed_track_id], limit=limit)
    return [{
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'url': track['external_urls']['spotify']
    } for track in recs['tracks']]

def get_top_tracks(sp, artist_id, country="US", limit=5):
    try:
        results = sp.artist_top_tracks(artist_id, country=country)
        return [{
            'id': track['id'],  # Include the track ID
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'url': track['external_urls']['spotify']
        } for track in results['tracks'][:limit]]
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return []
    except Exception as e:
        print(f"Error fetching top tracks: {e}")
        return []

#  RELATED ARTISTS
def get_related_artists(sp, artist_id):
    try:
        results = sp.artist_related_artists(artist_id)
        return [{
            'name': artist['name'],
            'url': artist['external_urls']['spotify']
        } for artist in results['artists']]
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return []
    except Exception as e:
        print(f"Error fetching related artists: {e}")
        return []

#  AUDIO FEATURES
def get_audio_features(sp, track_id):
    try:
        features = sp.audio_features([track_id])[0]
        if not features:
            raise ValueError("No audio features found for the track.")
        return {
            'danceability': features['danceability'],
            'energy': features['energy'],
            'tempo': features['tempo'],
            'valence': features['valence']
        }
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
        return None
    except Exception as e:
        print(f"Error fetching audio features: {e}")
        return None

def main():
    print("🎧 Welcome to the Music Discovery App")

    try:
        sp = create_spotify_client()
    except Exception as e:
        print("Auth error:", e)
        return

    query = input("\n Search for an artist: ")
    results = sp.search(q=query, type='artist', limit=1)
    if not results['artists']['items']:
        print("No artist found.")
        return

    artist = results['artists']['items'][0]
    print(f"\n Found artist: {artist['name']}")

    # Fetch and display the number of followers the artist has on Spotify
    total_tracks = artist['followers']['total']  # Approximation using followers
    print(f"\n {artist['name']} has approximately {total_tracks} followers on Spotify.")

    # Fetch top tracks for the artist
    top_tracks = get_top_tracks(sp, artist['id'])
    if not top_tracks:
        print("No top tracks found for this artist.")
        return

    print("\n Top Tracks:")
    for idx, track in enumerate(top_tracks, start=1):
        print(f"{idx}. {track['name']} by {track['artist']} - {track['url']}")

    # Allow the user to select a track to view its audio features
    try:
        track_choice = int(input("\n Select a track number to view its audio features (1-5): "))
        if track_choice < 1 or track_choice > len(top_tracks):
            print("Invalid choice. Exiting.")
            return
        selected_track = top_tracks[track_choice - 1]
        print(f"\n Selected Track: {selected_track['name']} by {selected_track['artist']}")

        # Fetch and display audio features for the selected track
        features = get_audio_features(sp, selected_track['id'])
        if not features:
            print("Unable to fetch audio features for the selected track.")
            return

        print("\n Audio Features:")
        for k, v in features.items():
            print(f"{k.title()}: {v}")
    except ValueError:
        print("Invalid input. Please enter a number.")

    # Fetch and display a related artist
    related_artists = get_related_artists(sp, artist['id'])
    if related_artists:
        related_artist = related_artists[0]  # Pick the first related artist
        print(f"\n You might also like: {related_artist['name']} - {related_artist['url']}")
    else:
        print("\n No similar artists found.")

if __name__ == "__main__":
    main()
