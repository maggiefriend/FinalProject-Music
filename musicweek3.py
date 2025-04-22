import os
import spotipy
import csv
import matplotlib.pyplot as plt
from spotipy.oauth2 import SpotifyClientCredentials

# AUTHENTICATION
def create_spotify_client():
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
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

#  AUDIO FEATURES
def get_audio_features(sp, track_id):
    features = sp.audio_features([track_id])[0]
    return {
        'danceability': features['danceability'],
        'energy': features['energy'],
        'tempo': features['tempo'],
        'valence': features['valence']
    }

# PLOT FEATURES
def plot_audio_features(features, title="Audio Features"):
    labels = list(features.keys())
    values = list(features.values())

    plt.figure(figsize=(8, 4))
    plt.bar(labels, values, color='skyblue')
    plt.title(title)
    plt.xlabel("Feature")
    plt.ylabel("Value")
    plt.ylim(0, max(values) + 10)
    plt.tight_layout()
    plt.show()


# SAVE TO CSV

def save_recommendations(recs, filename="recommendations.csv"):
    with open(filename, "w", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "artist", "url"])
        writer.writeheader()
        writer.writerows(recs)
    print(f"Recommendations saved to {filename}")


def main():
    print("🎧 Welcome to the Music Discovery App (Advanced Edition)")

    try:
        sp = create_spotify_client()
    except Exception as e:
        print("Auth error:", e)
        return

    query = input("\n Search for a song or artist: ")
    tracks = search_track(sp, query)

    if not tracks:
        print("No results found.")
        return

    print("\n Results:")
    for idx, t in enumerate(tracks):
        print(f"{idx + 1}. {t['name']} by {t['artist']}")

    try:
        choice = int(input("\n Pick a track number: ")) - 1
        selected = tracks[choice]
    except (IndexError, ValueError):
        print("Invalid choice.")
        return

    # Show audio features
    print(f"\n Audio features for '{selected['name']}' by {selected['artist']}:")
    features = get_audio_features(sp, selected['id'])
    for k, v in features.items():
        print(f"{k.title()}: {v}")
    plot_audio_features(features, title=selected['name'])

    # Get recommendations
    recs = get_recommendations(sp, selected['id'])
    print("\n You might also like:")
    for rec in recs:
        print(f"- {rec['name']} by {rec['artist']} - {rec['url']}")

    # Save option
    save = input("\n Save these recommendations to a CSV? (y/n): ").strip().lower()
    if save == 'y':
        save_recommendations(recs)

    print("\n Done! Thanks for using the app.")

if __name__ == "__main__":
    main()

