import sqlite3
import json
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional


class Db:

    COLUMN_NAMES = ("valence", "year", "acousticness", "artists", "danceability", "duration_ms", "energy", "id", "instrumentalness", "liveness", "mode", "name", "popularity", "speechiness", "tempo", "genres")
    db_path = os.path.join("data", "database.db")

    def __init__(self) -> None:
        pass

    def load_songs_dataset(self) -> None:
        """Loads the Spotify songs and genres datasets from a local SQLite database."""
        
        conn = sqlite3.connect(os.path.join("data", "database.db"))

        # songs_dataset = pd.read_sql_query(
        #     "SELECT year, artists, danceability, energy, id, instrumentalness, name, popularity, tempo, genres FROM songs_w_genres",
        #     conn,
        # )

        
        songs_dataset = pd.read_sql_query(
            "SELECT * FROM songs_w_genres",
            conn,
        )

        conn.close()
        return songs_dataset
    
    def load_artist_genres_dataset(self):
        """Loads the Spotify songs and genres datasets from a local SQLite database."""
        
        conn = sqlite3.connect(Db.db_path)

        artists_genres_dataset = pd.read_sql_query(
            "SELECT * FROM artists_genres", conn
        )
        conn.close()
        return artists_genres_dataset

    # def is_in_database(self, id):    
    #     with sqlite3.connect(Db.db_path) as conn:
    #         cur = conn.cursor()
    #         return cur.execute('SELECT * FROM songs_w_genres WHERE id = ?', (id,)).fetchone()
    
    def fetch_song(self, id): 
        with sqlite3.connect(Db.db_path) as conn:
            cur = conn.cursor()
            # song = pd.read_sql_query('SELECT * FROM songs_w_genres WHERE id = :id', conn, params={'id': id})
            # return song
            song_data = cur.execute('SELECT * FROM songs_w_genres WHERE id = ?', (id,)).fetchone()
            if song_data:
                return {record[0]: record[1] for record in  zip(Db.COLUMN_NAMES, song_data)}
            return None
    
        
    def insert_song_into_db(self, song):
        with sqlite3.connect(Db.db_path) as conn:
            cur = conn.cursor()
            count = cur.execute('''
                            INSERT INTO songs_w_genres 
                            ("valence", "year", "acousticness", "artists", "danceability", "duration_ms", "energy", "id", 
                            "instrumentalness", "liveness", "mode", "name", "popularity", "speechiness", "tempo", "genres") 
                            VALUES 
                            (:valence, 
                            :year, 
                            :acousticness, 
                            :artists, 
                            :danceability, 
                            :duration_ms, 
                            :energy, 
                            :id, 
                            :instrumentalness, 
                            :liveness, 
                            :mode, 
                            :name, 
                            :popularity, 
                            :speechiness, 
                            :tempo,
                            :genres);''', song)

            conn.commit()
            cur.close()
