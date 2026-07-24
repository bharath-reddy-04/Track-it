"""Server-only personalized recommendation endpoint."""

import asyncio
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException

from app.schemas.movie import RecommendationResponse
from app.services import customer_service, recommendation_service, tmdb_service
from app.services.recommendation_service import RecommendationModelError
from app.services.tmdb_service import TMDBServiceError

router = APIRouter(prefix="/api/recommendations", tags=["recommendations"])


def _recent_ids(movies: list[dict]) -> list[int]:
    def time(movie: dict):
        try:
            return datetime.fromisoformat(movie.get("clicked_at", "").replace("Z", "+00:00"))
        except (AttributeError, ValueError):
            return datetime.min.replace(tzinfo=timezone.utc)

    ids, seen = [], set()
    for movie in sorted(movies, key=time, reverse=True):
        movie_id = movie.get("id")
        if isinstance(movie_id, int) and movie_id not in seen:
            ids.append(movie_id)
            seen.add(movie_id)
        if len(ids) == 10:
            break
    return ids


@router.get("/{customer_id}", response_model=RecommendationResponse)
async def get_recommendations(customer_id: str):
    customer = customer_service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    clicked_movies = customer.get("movies") or []
    recent_ids = _recent_ids(clicked_movies)
    if not recent_ids:
        return {"recommendations": []}

    try:
        candidate_ids = await asyncio.to_thread(recommendation_service.recommend, recent_ids)
    except RecommendationModelError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc

    clicked_ids = {movie.get("id") for movie in clicked_movies if isinstance(movie, dict)}
    unseen_ids = [movie_id for movie_id in candidate_ids if movie_id not in clicked_ids]
    try:
        movies = await asyncio.gather(*(tmdb_service.get_movie_details(movie_id) for movie_id in unseen_ids))
    except TMDBServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    return {"recommendations": movies}
