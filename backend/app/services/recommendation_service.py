"""Load and query the pre-trained recommendation model."""

import os
from functools import lru_cache
from pathlib import Path

import joblib

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MODEL_PATH = PROJECT_ROOT / "backend" / "models" / "content_recommender.joblib"


class RecommendationModelError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _model():
    """Load the persisted artifact once per API process; never train in a request."""
    model_path = Path(os.getenv("RECOMMENDER_MODEL_PATH", DEFAULT_MODEL_PATH))
    if not model_path.is_file():
        raise RecommendationModelError(
            f"Pre-trained recommendation model not found: {model_path}. "
            "Run `backend/myenv/bin/python recomendation-engine/train_model.py` before starting the API."
        )
    try:
        return joblib.load(model_path)
    except Exception as exc:
        raise RecommendationModelError(f"Could not load pre-trained recommendation model: {exc}") from exc


def recommend(movie_ids: list[int], top_k: int = 10) -> list[int]:
    """Return ranked TMDB IDs using the previously trained model artifact."""
    try:
        model = _model()
        known_ids = [movie_id for movie_id in movie_ids if movie_id in model.id_to_row]
        if not known_ids:
            return []
        result = model.recommend_multiple(known_ids, top_k=top_k)
        return [int(movie_id) for movie_id in result["id"].tolist()]
    except RecommendationModelError:
        raise
    except Exception as exc:
        raise RecommendationModelError(f"Recommendation prediction failed: {exc}") from exc
