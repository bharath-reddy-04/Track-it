"""Lazy, process-local adapter for the project's content-based model."""

import importlib.util
from functools import lru_cache
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = PROJECT_ROOT / "recomendation-engine" / "recomendation.py"
DATASET_PATH = MODEL_PATH.with_name("tmdb_movies_clean.csv")


class RecommendationModelError(RuntimeError):
    pass


@lru_cache(maxsize=1)
def _model():
    if not DATASET_PATH.is_file():
        raise RecommendationModelError(f"Recommendation dataset not found: {DATASET_PATH}")

    spec = importlib.util.spec_from_file_location("local_recommendation_model", MODEL_PATH)
    if not spec or not spec.loader:
        raise RecommendationModelError(f"Could not load model from {MODEL_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.content_based(DATASET_PATH)


def recommend(movie_ids: list[int], top_k: int = 10) -> list[int]:
    """Return up to ten ranked TMDB IDs; IDs absent from the CSV are ignored."""
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
        raise RecommendationModelError(f"Recommendation model failed: {exc}") from exc
