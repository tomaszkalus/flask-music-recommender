from spotipy_data_access import SpotifyDataAccess
from db_data_access import Db

def recommend(spotify_data, songs_ids):
    spotify_dao = SpotifyDataAccess()
    db = Db()
    for id in songs_ids:
        if db.is_in_database(id):
            
        song = spotify_dao.fetch_song(id)
        print(song)
        db.insert_song_into_db(song)

