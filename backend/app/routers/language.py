"""
language.py
-----------
GET /api/language/{language_code}

Returns Popular/Top Rated/genre rows filtered to movies originally made in
the given language (TMDB's with_original_language), fetched concurrently.
"""


import asyncio
import re
import requests
from requests.exceptions import RequestException

from fastapi import APIRouter, HTTPException

from app.schemas.movie import LanguageResponse
from app.services import tmdb_service
from app.services.tmdb_service import TMDBServiceError
from app.utils.constants import GENRE_IDS

router = APIRouter(prefix="/api", tags=["language"])

# ISO 639-1 codes are exactly two lowercase letters (en, hi, te, ...).
_LANGUAGE_CODE_PATTERN = re.compile(r"^[a-z]{2}$")




@router.get("/language/{language_code}", response_model=LanguageResponse)
async def get_language_movies(language_code: str):
    language_code = language_code.lower()

    if not _LANGUAGE_CODE_PATTERN.match(language_code):
        raise HTTPException(
            status_code=400,
            detail=f"'{language_code}' is not a valid ISO 639-1 language code (expected 2 letters, e.g. 'en', 'te').",
        )

    lang_filter = {"with_original_language": language_code}

    try:
        (
            popular,
            top_rated,
            action,
            comedy,
            horror,
            romance,
            animation,
        ) = await asyncio.gather(
            tmdb_service.get_popular_movies(lang_filter),
            tmdb_service.get_top_rated_movies(lang_filter),
            tmdb_service.get_movies_by_genre(GENRE_IDS["action"], lang_filter),
            tmdb_service.get_movies_by_genre(GENRE_IDS["comedy"], lang_filter),
            tmdb_service.get_movies_by_genre(GENRE_IDS["horror"], lang_filter),
            tmdb_service.get_movies_by_genre(GENRE_IDS["romance"], lang_filter),
            tmdb_service.get_movies_by_genre(GENRE_IDS["animation"], lang_filter),
        )
    except TMDBServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return {
        "popular": popular,
        "topRated": top_rated,
        "action": action,
        "comedy": comedy,
        "horror": horror,
        "romance": romance,
        "animation": animation,
    }