from flask import Flask, request, jsonify, abort, render_template, redirect, url_for
import json
from recommender import Recommender
from recommender_system import RecommendationSystem
import pandas as pd
import pickle
from datetime import datetime
from spotify_track_search import spotify_search

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

@app.route("/", methods=['GET'])
def main():
    return render_template('index.html')
    
@app.route('/example')
def example():
    songs = pickle.load( open( "example_recommendations.p", "rb" ) )
    return render_template('recommendations_v3.html', songs=songs)
    
@app.route("/show_recommendations")
def recommend():
    data = request.args
    user_songs = []

    # i = 1
    # while True:
    #     song = {}
    #     artist = data.get(f'artist{i}')
    #     song_name = data.get(f'name{i}')
    #     if not artist or not song_name:
    #         break
    #     song['artist'] = artist
    #     song['name'] = song_name
    #     user_songs.append(song)
    #     i += 1

    i = 1
    while True:
        id = data.get(f'id{i}')
        if not id:
            break
        user_songs.append(id)
        i += 1

    # recommender = Recommender()
    recommender_system = RecommendationSystem()
        
    # recommended_songs = recommender.recommend(user_songs, 10)
    recommended_songs = recommender_system.recommend(user_songs)

    recommended_songs['artists'] = recommended_songs['artists'].apply(lambda x: json.loads(x))
    recommended_songs['genres'] = recommended_songs['genres'].apply(lambda x: json.loads(x))

    recommended_songs = recommended_songs.to_dict(orient='records')
    pickle.dump( recommended_songs, open( "example_recommendations.p", "wb" ) )
    return render_template('recommendations_v3.html', songs=recommended_songs)

@app.route("/search/<search_query>")
def search(search_query):
    # print(search_query)
    suggestions = spotify_search(search_query)
    return json.dumps(suggestions)

@app.route('/autocomplete_test')
def test():
    return render_template('index_autocomplete.html')