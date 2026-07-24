import numpy as np
import ast
import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import vstack


def parse_names(text, key="name"):
    if pd.isna(text) or text in ("", "[]"):
        return ""
    try:
        items = ast.literal_eval(text)
        return " ".join(str(i[key]).replace(" ", "") for i in items if key in i)
    except (ValueError, SyntaxError):
        return ""


def build_text_column(df: pd.DataFrame, text_cols=("overview", "genres", "keywords", "tagline",
                       "production_companies", "production_countries", "spoken_languages"),
                       dict1=None) -> pd.Series:

    combined = pd.Series([""] * len(df), index=df.index)
    for col in text_cols:
        if col not in df.columns:
            continue
        sample = df[col].dropna().astype(str).head(1)
        looks_like_json = len(sample) and sample.iloc[0].strip().startswith("[")
        values = df[col].apply(parse_names) if looks_like_json else df[col].fillna("")
        combined = combined + " " + values.astype(str).apply(lambda x: (" " + x) * dict1.get(col, 1))

    return combined


def vectorize(text: pd.Series, ngram_range=(1, 2), min_df=3, max_df=0.8, sublinear_tf=True, max_features=50000):
    """TF-IDF vectorize. Returns (sparse_matrix, fitted_vectorizer)."""
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=ngram_range,
        min_df=min_df,
        max_df=max_df,
        sublinear_tf=sublinear_tf,
        max_features=max_features
    )
    matrix = vectorizer.fit_transform(text)  # sparse (n, max_features)
    return matrix, vectorizer


class SimpleRecommender:
    def __init__(self, df: pd.DataFrame, matrix):

        self.df = df.reset_index(drop=True)
        self.matrix = matrix

        # NearestNeighbors on the sparse matrix: no full similarity matrix
        # ever gets built, so this scales to very large datasets.
        self.model = NearestNeighbors(metric="cosine", algorithm="brute")
        self.model.fit(self.matrix)

        self.id_to_row = dict(zip(self.df["id"], self.df.index))

    def recommend(self, movie_id, top_k=10):
        if movie_id not in self.id_to_row:
            raise ValueError(f"movie_id {movie_id} not found")

        row = self.id_to_row[movie_id]
        distances, indices = self.model.kneighbors(
            self.matrix[row], n_neighbors=min(top_k + 1, len(self.df))
        )

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == row:
                continue
            results.append((self.df.loc[idx, "id"], self.df.loc[idx, "title"], 1 - dist))

        return pd.DataFrame(results[:top_k], columns=["id", "title", "similarity"])

    def recommend_multiple(self, movie_ids, top_k=10):
        scores = {}

        for movie_id in movie_ids:
            recs = self.recommend(movie_id, top_k=100)

            for _, row in recs.iterrows():
                mid = row["id"]

                if mid in movie_ids:
                    continue

                scores[mid] = scores.get(mid, 0) + row["similarity"]

        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)

        results = []

        for mid, score in ranked[:top_k]:
            title = self.df.loc[self.id_to_row[mid], "title"]
            results.append((mid, title, score))

        return pd.DataFrame(results, columns=["id", "title", "score"])


def content_based(data_path=None):
    data_path = Path(data_path) if data_path else Path(__file__).with_name("tmdb_movies_clean.csv")
    movies = pd.read_csv(data_path, low_memory=False)
    movies = movies[(movies["vote_count"] >= 500) & (movies["vote_average"] >= 6.5) &
                     (movies.status == "Released") & (movies.adult == False) &
                     (movies.runtime > 60)]

    text = build_text_column(
        movies,
        text_cols=["overview", "genres", "keywords", "tagline", "production_companies",
                   "production_countries", "spoken_languages"],
        dict1={"overview": 2, "genres": 5, "keywords": 8, "tagline": 2,
               "production_companies": 1, "production_countries": 1, "spoken_languages": 1}
    )
    matrix, vectorizer = vectorize(text, max_features=20000)

    return SimpleRecommender(movies, matrix)


if __name__ == "__main__":
    rec = content_based()
    print(rec.recommend_multiple(movie_ids=[438631, 76600, 679, 157336], top_k=10))
