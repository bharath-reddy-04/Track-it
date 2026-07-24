"""
genre.py
--------
GET /api/genre/{genre}

Returns Trending/Popular/Top Rated rows scoped to a single genre, fetched
concurrently.
"""

import asyncio

from fastapi import APIRouter, HTTPException

from app.schemas.movie import GenreResponse
from app.services import tmdb_service
from app.services.tmdb_service import TMDBServiceError
from app.utils.constants import GENRE_IDS

router = APIRouter(prefix="/api", tags=["genre"])


@router.get("/genre/{genre}", response_model=GenreResponse)
async def get_genre_movies(genre: str):
    genre_key = genre.lower()

    if genre_key not in GENRE_IDS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown genre '{genre}'. Available genres: {', '.join(GENRE_IDS.keys())}",
        )

    genre_filter = {"with_genres": GENRE_IDS[genre_key]}

    try:
        trending, popular, top_rated = await asyncio.gather(
            tmdb_service.get_trending_movies(genre_filter),
            tmdb_service.get_popular_movies(genre_filter),
            tmdb_service.get_top_rated_movies(genre_filter),
        )
    except TMDBServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return {"trending": trending, "popular": popular, "topRated": top_rated}