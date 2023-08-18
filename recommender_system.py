from spotipy_data_access import SpotifyDataAccess
from db_data_access import Db
from recommender import Recommender
import pandas as pd
# import json
import orjson as json
import time

class RecommendationSystem:
    def __init__(self) -> None:
        self.spotify_data_access = SpotifyDataAccess()
        self.db = Db()
        self.user_songs_data = None


    def get_user_songs_data(self, songs_ids):
        
        user_songs_data = []
        user_songs_artists = set()
        user_songs_genres = set()
        
        for id in songs_ids:
            print(f"Fetching for song with id: {id}")
            if (song := self.db.fetch_song(id)):
                print('Loaded song from the DB')

            elif (song := self.spotify_data_access.fetch_song(id)):
                self.db.insert_song_into_db(song)
                print('Loaded song from API')

            else: 
                print(f"Song with the id of: {id} couldn't be found neither in the DB nor in the Spotify API.")
                continue
            user_songs_data.append(song)
            user_songs_artists.update(json.loads(song["artists"]))
            user_songs_genres.update(json.loads(song["genres"]))

        user_songs_df = pd.DataFrame(user_songs_data)
        print(user_songs_data)

        return user_songs_df, user_songs_artists, user_songs_genres
    
    def recommend(self, songs_ids):
        user_songs_data = self.get_user_songs_data(songs_ids)

        user_songs_df = user_songs_data[0]
        user_songs_artists = user_songs_data[1]
        user_songs_genres = user_songs_data[2]

        songs_dataset = self.db.load_songs_dataset()
        artists_genres_dataset = self.db.load_artist_genres_dataset()


        # user_songs_df = pd.DataFrame.from_dict(user_songs_data)
        recommender = Recommender(songs_dataset, artists_genres_dataset)

        recommendations = recommender.recommend(user_songs_df, user_songs_artists, user_songs_genres, 10)
        print(recommendations)
        return recommendations

