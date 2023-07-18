from flask import Flask, request, jsonify, abort
import json

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/recommend", methods=["POST"])
def recommend():
    if request.headers.get('Content-Type') != "application/json":
        abort(404)

    songs = ""
    for record in request.json["songs"]:
        songs += f"{record['artist']} - {record['song']}<br>"
    return songs
