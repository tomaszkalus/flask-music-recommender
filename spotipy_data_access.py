import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from pprint import pprint
import json

class SpotifyDataAccess:
    def __init__(self) -> None:
        api_id = os.environ.get('spotify_api_id')
        api_secret = os.environ.get('spotify_api_secret')
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=api_id,
                                                                client_secret=api_secret))
        

    def autocomplete_search(self, query: str):
        results = self.sp.search(q=query, limit=10)

        suggestions = []

        print(results)

        for idx, track in enumerate(results['tracks']['items']):
            artists = ', '.join([t['name'] for t in track['artists']])
            mapped_song = {'artists': artists, 'name': track['name'], 'id': track['id']  }
            suggestions.append(mapped_song)

        return suggestions
    
    def fetch_song_genres(self, artists_ids: list):
        genres = set()
        for artist_id in artists_ids:
            artist = self.sp.artist(artist_id)
            song_genres = artist['genres']
            genres.update(set(song_genres))
            # print(f'{artist["name"]} - {", ".join(song_genres)}')
        return genres
    
    def fetch_song(self, song_id):
        features = self.sp.audio_features([song_id])[0]
        song_data = self.sp.track(song_id)
        print(song_data)
        artists_ids = [artist['id'] for artist in song_data['artists']]
        artists_names = [artist['name'] for artist in song_data['artists']]
        song_genres = self.fetch_song_genres(artists_ids)
        self.fetch_song_genres(artists_ids)
        song_obj = {
            'valence': features['valence'],
            'year': song_data['album']['release_date'].split('-')[0],
            'acousticness': features['acousticness'],
            'artists': json.dumps(artists_names),
            'danceability': features['danceability'],
            'duration_ms': song_data['duration_ms'],
            'energy': features['energy'],
            'explicit': int(song_data['explicit']),
            'id': song_id,
            'instrumentalness': features['instrumentalness'],
            'liveness': features['liveness'],
            'mode': features['mode'],
            'name': song_data['name'],
            'popularity': song_data['popularity'],
            'speechiness': features['speechiness'],
            'tempo': features['tempo'],
            'genres': json.dumps(list(song_genres))
        }
        return song_obj
    

# sda = SpotifyDataAccess()
# res = sda.fetch_song('3RZvLFnyQTBU92Xu85UX2s')
# pprint(res)
        
