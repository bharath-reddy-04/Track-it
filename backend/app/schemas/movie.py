"""
movie.py
--------
Pydantic schemas describing API responses. Keeping these separate from the
routers means the response "shape" is documented in one place and reused
by FastAPI's response_model validation + auto-generated OpenAPI docs.
"""

from typing import List, Optional
from pydantic import BaseModel


class Movie(BaseModel):
    """A single movie as returned by TMDB, trimmed to the fields the
    frontend's Card/MovieRow components actually use."""

    id: int
    title: Optional[str] = None
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    vote_average: Optional[float] = None
    release_date: Optional[str] = None
    overview: Optional[str] = None
    original_language: Optional[str] = None
    genre_ids: List[int] = []


class RecommendationResponse(BaseModel):
    recommendations: List[Movie]


class HomeResponse(BaseModel):
    """Shape returned by GET /api/home."""

    trending: List[Movie]
    popular: List[Movie]
    topRated: List[Movie]
    action: List[Movie]
    comedy: List[Movie]
    horror: List[Movie]
    romance: List[Movie]
    animation: List[Movie]


class LanguageResponse(BaseModel):
    """Shape returned by GET /api/language/{language_code}."""

    popular: List[Movie]
    topRated: List[Movie]
    action: List[Movie]
    comedy: List[Movie]
    horror: List[Movie]
    romance: List[Movie]
    animation: List[Movie]


class GenreResponse(BaseModel):
    """Shape returned by GET /api/genre/{genre}.

    Note: this returns Trending/Popular/Top Rated *within* the requested
    genre, rather than repeating every Home category re-filtered by the
    same genre (which would be redundant — the "action" row on a page
    already scoped to Action would just duplicate the "popular" row).
    """

    trending: List[Movie]
    popular: List[Movie]
    topRated: List[Movie]


class OTTResponse(BaseModel):
    """Shape returned by GET /api/ott/{provider}."""

    popular: List[Movie]
    topRated: List[Movie]
    action: List[Movie]
    comedy: List[Movie]
    romance: List[Movie]
    animation: List[Movie]


class ErrorResponse(BaseModel):
    """Standard error body returned for 4xx/5xx responses."""

    detail: str
