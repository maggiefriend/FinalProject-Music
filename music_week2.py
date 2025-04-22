import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

# AUTHENTICATION SETUP
def create_spotify_client():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise ValueError("Missing Spotify API credentials in environment variables.")

    auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

#  SEARCH FUNCTION
def search_track(sp, query, limit=5):
    results = sp.search(q=query, limit=limit, type='track')
    tracks = []
    for item in results['tracks']['items']:
        track_info = {
            'id': item['id'],
            'name': item['name'],
            'artist': item['artists'][0]['name'],
            'album': item['album']['name'],
            'url': item['external_urls']['spotify']
        }
        tracks.append(track_info)
    return tracks


#  RECOMMENDATION FUNCTION
def get_recommendations(sp, seed_track_id, limit=5):
    recommendations = sp.recommendations(seed_tracks=[seed_track_id], limit=limit)
    return [
        {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'url': track['external_urls']['spotify']
        }
        for track in recommendations['tracks']
    ]

def main():
    print("🎧 Welcome to the Music Discovery App 🎧")

    try:
        sp = create_spotify_client()
    except Exception as e:
        print("Error initializing Spotify client:", e)
        return

    query = input("\n Enter a song or artist to search: ")
    tracks = search_track(sp, query)

    if not tracks:
        print("No results found.")
        return

    print("\n Top Results:")
    for idx, track in enumerate(tracks):
        print(f"{idx + 1}. {track['name']} by {track['artist']} - {track['url']}")

    try:
        choice = int(input("\n Pick a track number to get recommendations: ")) - 1
        seed_track_id = tracks[choice]['id']
    except (IndexError, ValueError):
        print("Invalid choice.")
        return

    recs = get_recommendations(sp, seed_track_id)
    print("\n You might also like:")
    for rec in recs:
        print(f"- {rec['name']} by {rec['artist']} - {rec['url']}")

if __name__ == "__main__":
    main()

