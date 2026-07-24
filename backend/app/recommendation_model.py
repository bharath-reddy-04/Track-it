"""Trainable content-based movie recommender.

This module intentionally contains no web-framework code so its fitted model can
be serialized during the offline training step and loaded by the API process.
"""

import ast

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


def _parse_names(value: object, key: str = "name") -> str:
    if pd.isna(value) or value in ("", "[]"):
        return ""
    try:
        items = ast.literal_eval(str(value))
        return " ".join(str(item[key]).replace(" ", "") for item in items if key in item)
    except (ValueError, SyntaxError):
        return ""


def _build_text_column(movies: pd.DataFrame) -> pd.Series:
    weights = {
        "overview": 2,
        "genres": 5,
        "keywords": 8,
        "tagline": 2,
        "production_companies": 1,
        "production_countries": 1,
        "spoken_languages": 1,
    }
    combined = pd.Series("", index=movies.index, dtype="object")
    for column, weight in weights.items():
        if column not in movies:
            continue
        sample = movies[column].dropna().astype(str).head(1)
        is_structured = bool(len(sample) and sample.iloc[0].strip().startswith("["))
        values = movies[column].apply(_parse_names) if is_structured else movies[column].fillna("")
        combined = combined + " " + (" " + values.astype(str)) * weight
    return combined


class SimpleRecommender:
    """Fitted recommender persisted by the offline training command."""

    def __init__(self, movies: pd.DataFrame, matrix) -> None:
        self.movies = movies.reset_index(drop=True)
        self.matrix = matrix
        self.model = NearestNeighbors(metric="cosine", algorithm="brute")
        self.model.fit(matrix)
        self.id_to_row = {int(movie_id): row for row, movie_id in enumerate(self.movies["id"])}

    def recommend(self, movie_id: int, top_k: int = 10) -> pd.DataFrame:
        if movie_id not in self.id_to_row:
            raise ValueError(f"movie_id {movie_id} not found")
        row = self.id_to_row[movie_id]
        distances, indices = self.model.kneighbors(self.matrix[row], n_neighbors=min(top_k + 1, len(self.movies)))
        results = [
            (int(self.movies.iloc[index]["id"]), self.movies.iloc[index]["title"], float(1 - distance))
            for distance, index in zip(distances[0], indices[0])
            if index != row
        ]
        return pd.DataFrame(results[:top_k], columns=["id", "title", "similarity"])

    def recommend_multiple(self, movie_ids: list[int], top_k: int = 10) -> pd.DataFrame:
        selected = set(movie_ids)
        scores: dict[int, float] = {}
        for movie_id in selected:
            if movie_id not in self.id_to_row:
                continue
            for _, recommendation in self.recommend(movie_id, top_k=100).iterrows():
                candidate_id = int(recommendation["id"])
                if candidate_id not in selected:
                    scores[candidate_id] = scores.get(candidate_id, 0.0) + float(recommendation["similarity"])
        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)[:top_k]
        return pd.DataFrame(
            [(movie_id, self.movies.iloc[self.id_to_row[movie_id]]["title"], score) for movie_id, score in ranked],
            columns=["id", "title", "score"],
        )


def train_recommender(data_path: str) -> SimpleRecommender:
    """Fit the model from a CSV. Call only from the offline training command."""
    movies = pd.read_csv(data_path, low_memory=False)
    movies = movies[
        (movies["vote_count"] >= 500)
        & (movies["vote_average"] >= 6.5)
        & (movies["status"] == "Released")
        & (movies["adult"] == False)  # noqa: E712 - pandas vector comparison
        & (movies["runtime"] > 60)
    ].copy()
    text = _build_text_column(movies)
    vectorizer = TfidfVectorizer(
        stop_words="english", ngram_range=(1, 2), min_df=3, max_df=0.8, sublinear_tf=True, max_features=20_000
    )
    return SimpleRecommender(movies, vectorizer.fit_transform(text))
