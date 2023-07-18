import pandas as pd
import sqlite3
import json
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
import time

class Recommender:
    def __init__(self) -> None:
        self.__load_dataset_from_db()

    def __load_dataset_from_db(self):
        conn = sqlite3.connect(os.path.join('data', 'database.db'))
        self.songs_dataset = pd.read_sql_query("SELECT year, artists, danceability, energy, id, instrumentalness, name, popularity, tempo, genres FROM songs_w_genres", conn)
        self.artists_genres_dataset = pd.read_sql_query("SELECT * FROM artists_genres", conn)
        conn.close()

    def __get_song_data(self, song):
        try:
            song_data = self.songs_dataset[(self.songs_dataset['name'] == song['name'])  & (self.songs_dataset['artists'].str.contains(song['artist']))]
            song_data_numeric = song_data.select_dtypes(exclude='object').iloc[0]
            return song_data_numeric
        
        except IndexError:
            return None
        

    def __get_artists_genres(self, artists_list: list):
        genres = set()
        for artist in artists_list:
            artist_data = self.artists_genres_dataset.loc[self.artists_genres_dataset["artists"] == artist]
            artist_genres_json = artist_data["genres"].values[0]
            artist_genres = json.loads(artist_genres_json)
            genres.update(artist_genres)
        return genres

    def __calculate_features_means(self, song_list):
        song_vectors = []
        for song in song_list: 
            song_data = self.__get_song_data(song)
            if song_data is None:
                print('Warning: {} does not exist in database'.format(song['name']))
                continue
            song_vectors.append(song_data)  

        df = pd.concat(song_vectors, axis=1)
        mean_series = df.mean(axis=1)
        return mean_series
    

    def __calculate_genres_compatibility(self, genres):
        ''' Oblicza kompatybilność ze względu na gatunek muzyki '''
        self.songs_dataset['genre compatibility'] = self.songs_dataset['genres'].apply(lambda x: len(set(json.loads(x)) & set(genres)) / len(genres))
    
    def __get_n_recommended_songs(self, n):
        unique_artists = set()
        recommended_songs = []

        sorted_df = self.songs_dataset.sort_values('cosine_similarity', ascending=False)

        for _, record in sorted_df.iterrows():
            artist = record['artists']
            if artist not in unique_artists:
                recommended_songs.append(record)
                unique_artists.add(artist)

            if len(recommended_songs) == n:
                break

        return pd.DataFrame(recommended_songs)
    
    def __calculate_distances(self, input_features_vector):
        ''' Oblicza dystans metryką cosinusową od podanych wartości do każdej z piosenek w bazie i je zwraca '''

        scaler = MinMaxScaler()

        songs_dataset_numeric = self.songs_dataset.select_dtypes(exclude="object")

        scaler.fit(songs_dataset_numeric)
        normalized_data = pd.DataFrame(scaler.transform(songs_dataset_numeric), columns=songs_dataset_numeric.columns)
        normalized_input_vector = pd.DataFrame(scaler.transform([input_features_vector]), columns=songs_dataset_numeric.columns)

        self.songs_dataset["cosine_similarity"] = cosine_similarity(normalized_data, normalized_input_vector)

    def recommend(self, song_list: list, n: int):
        
        input_features_vector: pd.Series = self.__calculate_features_means(song_list)

        input_artists = [song["artist"] for song in song_list]
        target_genres = self.__get_artists_genres(input_artists)
        input_features_vector["genre_compatibility"] = 1

        self.__calculate_genres_compatibility(target_genres)

        self.__calculate_distances(input_features_vector)
        
        recommended_songs = self.__get_n_recommended_songs(n)

        

        return recommended_songs

start = time.time()
recommender = Recommender()
recommended = recommender.recommend([{"artist": "The Smiths", "name": "How Soon Is Now? - 2008 Remaster"}, {"artist": "The Cure", "name": "Lovesong"}], 10)

with open("recommendations", "w") as file:
    # Write the variable value to the file
    file.write(recommended.to_string())

# print(recommended)
print(f"Overall - {round(time.time() - start, 2)} s")
