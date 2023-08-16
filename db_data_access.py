import sqlite3
import json
import os
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from typing import Optional


class Db:

    db_path = os.path.join("data", "database.db")

    def __init__(self) -> None:
        pass

    def load_songs_dataset(self) -> None:
        """Loads the Spotify songs and genres datasets from a local SQLite database."""
        
        conn = sqlite3.connect(os.path.join("data", "database.db"))

        songs_dataset = pd.read_sql_query(
            "SELECT year, artists, danceability, energy, id, instrumentalness, name, popularity, tempo, genres FROM songs_w_genres",
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

    def is_in_database(self, id):    
        with sqlite3.connect(Db.db_path) as conn:
            cur = conn.cursor()
            return cur.execute('SELECT * FROM songs_w_genres WHERE id = ?', (id,)).fetchone()
        
    def insert_song_into_db(self, song):
        with sqlite3.connect(Db.db_path) as conn:
            cur = conn.cursor()
            count = cur.execute('''
                            INSERT INTO songs 
                            ("valence", "year", "acousticness", "artists", "danceability", "duration_ms", "energy", "explicit", "id", 
                            "instrumentalness", "liveness", "mode", "name", "popularity", "speechiness", "tempo") 
                            VALUES 
                            (:valence, 
                            :year, 
                            :acousticness, 
                            :artists, 
                            :danceability, 
                            :duration_ms, 
                            :energy, 
                            :explicit, 
                            :id, 
                            :instrumentalness, 
                            :liveness, 
                            :mode, 
                            :name, 
                            :popularity, 
                            :speechiness, 
                            :tempo);''', song)
            # print(count)
            conn.commit()
            cur.close()
            # conn.close()
        
    

# db = Db()
# print(db.is_id_in_database('7xPhfUan2yNtyFG0cUWkt8'))


