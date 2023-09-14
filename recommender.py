import orjson as json
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity


class Recommender:
    """Class for performing a feature-based recommendation using cosine similarity for a set of songs provided by the user."""

    def __init__(
        self, songs_dataset: pd.DataFrame) -> None:
        self.songs_dataset = songs_dataset

    def __calculate_features_means(self, song_list: pd.DataFrame) -> pd.Series:
        """Calculates the means of all the numeric features from the songs provided via an argument."""

        df = song_list.select_dtypes(exclude="object")
        mean_series = df.mean(axis=0)
        return mean_series

    def __calculate_genres_compatibility(self, genres: list) -> None:
        """Calculates number of genres that match the provided genres list divided by number of genres in that list for every song
        in a songs dataset and assigns that value to the 'genre compatibility' column.
        """

        try:
            self.songs_dataset["genre compatibility"] = self.songs_dataset["genres"].apply(lambda x: len(set(json.loads(x)) & genres) / len(genres))

        except ZeroDivisionError:
            self.songs_dataset["genre compatibility"] = 0

    def __get_n_recommended_songs(self, n: int) -> pd.DataFrame:
        """Sorts the dataset and gets n records with the highest cosine similarity, only allowing each artist to appear once."""
        unique_artists = set()
        recommended_songs = []

        sorted_df = self.songs_dataset.sort_values("cosine_similarity", ascending=False)

        for _, record in sorted_df.iterrows():
            artist = record["artists"]
            if artist not in unique_artists:
                recommended_songs.append(record)
                unique_artists.add(artist)

            if len(recommended_songs) == n:
                break

        return pd.DataFrame(recommended_songs)

    def __calculate_distances(self, input_features_vector: pd.Series) -> None:
        """Calculates the cosine similarity between the input features vector provided as an argument and assigns it to the dataframe."""

        scaler = MinMaxScaler()

        songs_dataset_numeric = self.songs_dataset.select_dtypes(exclude="object")

        scaler.fit(songs_dataset_numeric)

        normalized_data = pd.DataFrame(
            scaler.transform(songs_dataset_numeric),
            columns=songs_dataset_numeric.columns,
        )

        normalized_input_vector = pd.DataFrame(
            scaler.transform([input_features_vector]),
            columns=songs_dataset_numeric.columns,
        )

        self.songs_dataset["cosine_similarity"] = cosine_similarity(
            normalized_data, normalized_input_vector
        )

    def recommend(self, song_list: list, target_genres, n: int):
        """Performs a complete recommendation of n most similar songs based on the provided list of songs."""

        input_features_vector: pd.Series = self.__calculate_features_means(song_list)

        input_features_vector["genre_compatibility"] = 1

        self.__calculate_genres_compatibility(target_genres)
        self.__calculate_distances(input_features_vector)
        recommended_songs = self.__get_n_recommended_songs(n)

        return recommended_songs
