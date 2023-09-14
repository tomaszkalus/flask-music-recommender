import sqlite3
import json
import os
import pandas as pd
import sys

class Db:
    COLUMN_NAMES = (
        "valence",
        "year",
        "acousticness",
        "artists",
        "danceability",
        "duration_ms",
        "energy",
        "id",
        "instrumentalness",
        "liveness",
        "mode",
        "name",
        "popularity",
        "speechiness",
        "tempo",
        "genres",
    )
    db_path = os.path.join("data", "database.db")

    def __init__(self) -> None:
        pass

    def load_songs_dataset(self) -> None:
        """Loads the Spotify songs and genres datasets from a local SQLite database."""

        conn = sqlite3.connect(os.path.join("data", "database.db"))

        songs_dataset = pd.read_sql_query(
            "SELECT * FROM songs_w_genres",
            conn,
        )

        print("Size of songs dataset:")
        print(sys.getsizeof(songs_dataset))

        conn.close()
        return songs_dataset

    def load_artist_genres_dataset(self):
        """Loads the Spotify songs and genres datasets from a local SQLite database."""

        conn = sqlite3.connect(Db.db_path)

        artists_genres_dataset = pd.read_sql_query("SELECT * FROM artists_genres", conn)

        conn.close()
        return artists_genres_dataset

    def fetch_song(self, id):
        """Fetches the audio features and genres of a song with given Spotify ID."""

        with sqlite3.connect(Db.db_path) as conn:
            cur = conn.cursor()
            song_data = cur.execute(
                "SELECT * FROM songs_w_genres WHERE id = ?", (id,)
            ).fetchone()
            if song_data:
                song_dict = {
                    record[0]: record[1] for record in zip(Db.COLUMN_NAMES, song_data)
                }
                song_dict["genres"] = set(json.loads(song_dict["genres"]))
                song_dict["artists"] = set(json.loads(song_dict["artists"]))
                return song_dict
            return None

    def insert_song_into_db(self, song):
        with sqlite3.connect(Db.db_path) as conn:
            cur = conn.cursor()

            song["genres"] = json.dumps(list(song["genres"]))
            song["artists"] = json.dumps(list(song["artists"]))

            cur.execute(
                """
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
                :genres);""",
                song,
            )

            conn.commit()
            cur.close()
