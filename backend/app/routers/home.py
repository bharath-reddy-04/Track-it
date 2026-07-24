"""
home.py
-------
GET /api/home

Returns every category row shown on the Home page in one response, fetched
concurrently so the page isn't waiting on 8 sequential TMDB round-trips.
"""

import asyncio

from fastapi import APIRouter, HTTPException

from app.schemas.movie import HomeResponse
from app.services import tmdb_service
from app.services.tmdb_service import TMDBServiceError
from app.utils.constants import GENRE_IDS

router = APIRouter(prefix="/api", tags=["home"])


@router.get("/home", response_model=HomeResponse)
async def get_home_movies():
    try:
        (
            trending,
            popular,
            top_rated,
            action,
            comedy,
            horror,
            romance,
            animation,
        ) = await asyncio.gather(
            tmdb_service.get_trending_movies(),
            tmdb_service.get_popular_movies(),
            tmdb_service.get_top_rated_movies(),
            tmdb_service.get_movies_by_genre(GENRE_IDS["action"]),
            tmdb_service.get_movies_by_genre(GENRE_IDS["comedy"]),
            tmdb_service.get_movies_by_genre(GENRE_IDS["horror"]),
            tmdb_service.get_movies_by_genre(GENRE_IDS["romance"]),
            tmdb_service.get_movies_by_genre(GENRE_IDS["animation"]),
        )
    except TMDBServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return {
        "trending": trending,
        "popular": popular,
        "topRated": top_rated,
        "action": action,
        "comedy": comedy,
        "horror": horror,
        "romance": romance,
        "animation": animation,
    }