from flask import Flask, request, jsonify, abort, render_template, redirect, url_for
import json
from recommender import Recommender
import pandas as pd
from urllib.parse import urlsplit, parse_qs

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html')
    
    if request.method == 'POST':

        # print(request.data)
        if request.headers.get('Content-Type') != "application/json":
            abort(404)
        songs = request.get_json()
        print(songs)

        recommender = Recommender()
        
        recommended_songs = recommender.recommend(songs, 10)
        print(recommended_songs)
        recommended_songs['artists'] = recommended_songs['artists'].apply(lambda x: json.loads(x))
        recommended_songs['genres'] = recommended_songs['genres'].apply(lambda x: json.loads(x))

        recommended_songs = recommended_songs.to_json(orient='records')
        return recommended_songs

        # recommended_songs = recommended_songs.values.tolist()
        
        # return render_template('recommendations.html', songs=recommended_songs)


@app.route("/recommendations", methods=['POST'])
def show_recommendations():
    recommended_songs = request.args.get('recommended_songs', default=None)
    if recommended_songs is not None:
        recommended_songs = json.loads(recommended_songs)

    print(recommended_songs)
    return 'Hello'
    return render_template('recommendations.html', songs=recommended_songs)

@app.route("/show_recommendations/<path:songs>")
def recommend(songs):
    raw_songs = songs.split('/')
    songs = [{'artist': parse_qs(song)['artist'][0], 'name': parse_qs(song)['name'][0]} for song in raw_songs]


    print(songs)
    
    recommender = Recommender()
        
    recommended_songs = recommender.recommend(songs, 10)
    print(recommended_songs)
    recommended_songs['artists'] = recommended_songs['artists'].apply(lambda x: json.loads(x))
    recommended_songs['genres'] = recommended_songs['genres'].apply(lambda x: json.loads(x))

    # recommended_songs = recommended_songs.to_json(orient='records')
    recommended_songs = recommended_songs.to_dict(orient='records')
    print(recommended_songs)
    # return recommended_songs
    return render_template('recommendations.html', songs=recommended_songs)
