from flask import Flask, request, render_template
import json
from recommender_system import RecommendationSystem
from data_access.spotipy_data_access import SpotifyDataAccess
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(get_remote_address, app=app, default_limits=["500 per day", "150 per hour"])


@app.route("/", methods=['GET'])
def main():
    return render_template('index.html')


@app.route("/recommendations")
def recommend():
    data = request.args
    user_songs = []
    i = 1
    while True:
        id = data.get(f'id{i}')
        if not id:
            break
        user_songs.append(id)
        i += 1

    recommender_system = RecommendationSystem()

    recommended_songs = recommender_system.recommend(user_songs)

    recommended_songs['artists'] = recommended_songs['artists'].apply(
        lambda x: json.loads(x))
    recommended_songs['genres'] = recommended_songs['genres'].apply(
        lambda x: json.loads(x))

    recommended_songs = recommended_songs.to_dict(orient='records')
    return render_template('recommendations.html', songs=recommended_songs)


@app.route("/search/<search_query>")
@limiter.limit("60 per minute")
def search(search_query):
    spotify_dao = SpotifyDataAccess()
    suggestions = spotify_dao.autocomplete_search(search_query)
    return json.dumps(suggestions)
