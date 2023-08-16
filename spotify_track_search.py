import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

def spotify_search(userInput):
    api_id = os.environ.get('spotify_api_id')
    api_secret = os.environ.get('spotify_api_secret')

    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=api_id,
                                                            client_secret=api_secret))

    results = sp.search(q=userInput, limit=10)

    suggestions = []

    print(results)

    for idx, track in enumerate(results['tracks']['items']):
        artists = ', '.join([t['name'] for t in track['artists']])
        mapped_song = {'artists': artists, 'name': track['name'], 'id': track['id']  }
        suggestions.append(mapped_song)

    return suggestions

if __name__ == '__main__':
    query = 'Arabella'
    search = spotify_search(query)
    # print(search)