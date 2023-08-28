import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
import os


class SpotifyDataAccess:
    def __init__(self) -> None:
        api_id = os.environ.get("spotify_api_id")
        api_secret = os.environ.get("spotify_api_secret")
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=api_id, client_secret=api_secret
            )
        )

    def autocomplete_search(self, query: str):
        results = self.sp.search(q=query, limit=10)
        suggestions = []

        for track in results["tracks"]["items"]:
            artists = ", ".join([artist["name"] for artist in track["artists"]])
            mapped_song = {"artists": artists, "name": track["name"], "id": track["id"]}
            suggestions.append(mapped_song)

        return suggestions

    def fetch_song_genres(self, artists_ids: list):
        genres = set()
        for artist_id in artists_ids:
            artist = self.sp.artist(artist_id)
            song_genres = artist["genres"]
            genres.update(set(song_genres))
        return genres

    def fetch_song(self, song_id):
        features = self.sp.audio_features([song_id])[0]
        try:
            song_data = self.sp.track(song_id)
        except SpotifyException:
            return None
        artists_ids = [artist["id"] for artist in song_data["artists"]]
        artists_names = set([artist["name"] for artist in song_data["artists"]])
        song_genres = self.fetch_song_genres(artists_ids)
        self.fetch_song_genres(artists_ids)

        song_obj = {
            "valence": features["valence"],
            "year": int(song_data["album"]["release_date"].split("-")[0]),
            "acousticness": features["acousticness"],
            "artists": artists_names,
            "danceability": features["danceability"],
            "duration_ms": song_data["duration_ms"],
            "energy": features["energy"],
            "id": song_id,
            "instrumentalness": features["instrumentalness"],
            "liveness": features["liveness"],
            "mode": features["mode"],
            "name": song_data["name"],
            "popularity": song_data["popularity"],
            "speechiness": features["speechiness"],
            "tempo": features["tempo"],
            "genres": set(song_genres),
        }
        return song_obj
    