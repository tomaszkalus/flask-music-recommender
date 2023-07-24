from dataclasses import dataclass

@dataclass
class Song:
    artist_name: str
    song_name: str

    def __init__(self, name, age):
        self.name = name
        self.age = age
