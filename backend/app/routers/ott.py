"""
ott.py
------
GET /api/ott/{provider}

Returns Popular/Top Rated/genre rows filtered to movies available on the
given OTT platform (TMDB with_watch_providers + watch_region), fetched
concurrently.
"""

import asyncio

from fastapi import APIRouter, HTTPException

from app.core.config import settings
from app.schemas.movie import OTTResponse
from app.services import tmdb_service
from app.services.tmdb_service import TMDBServiceError
from app.utils.constants import GENRE_IDS, OTT_PROVIDER_IDS

router = APIRouter(prefix="/api", tags=["ott"])


@router.get("/ott/{provider}", response_model=OTTResponse)
async def get_ott_movies(provider: str):
    provider_key = provider.lower()

    if provider_key not in OTT_PROVIDER_IDS:
        raise HTTPException(
            status_code=404,
            detail=f"Unknown OTT provider '{provider}'. Available providers: {', '.join(OTT_PROVIDER_IDS.keys())}",
        )

    provider_id = OTT_PROVIDER_IDS[provider_key]
    provider_filter = {
        "with_watch_providers": provider_id,
        "watch_region": settings.DEFAULT_WATCH_REGION,
    }

    try:
        (
            popular,
            top_rated,
            action,
            comedy,
            romance,
            animation,
        ) = await asyncio.gather(
            tmdb_service.get_popular_movies(provider_filter),
            tmdb_service.get_top_rated_movies(provider_filter),
            tmdb_service.get_movies_by_genre(GENRE_IDS["action"], provider_filter),
            tmdb_service.get_movies_by_genre(GENRE_IDS["comedy"], provider_filter),
            tmdb_service.get_movies_by_genre(GENRE_IDS["romance"], provider_filter),
            tmdb_service.get_movies_by_genre(GENRE_IDS["animation"], provider_filter),
        )
    except TMDBServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return {
        "popular": popular,
        "topRated": top_rated,
        "action": action,
        "comedy": comedy,
        "romance": romance,
        "animation": animation,
    }