"""
tmdb_service.py
----------------
The ONLY module in this backend that talks to TMDB. Every router calls
functions defined here instead of building TMDB URLs itself — this is what
keeps TMDB request logic from being duplicated across routers, and is the
single place to change if TMDB's API ever changes.
"""

import asyncio
from typing import Optional

import httpx

from app.core.config import settings

# A page can issue eight TMDB requests at once. Limit the number of simultaneous
# connections so that transient TLS connection failures do not fail the whole page.
_request_semaphore = asyncio.Semaphore(settings.TMDB_MAX_CONCURRENT_REQUESTS)
_client = httpx.AsyncClient(
    timeout=settings.TMDB_TIMEOUT_SECONDS,
    limits=httpx.Limits(max_connections=1, max_keepalive_connections=1),
)



class TMDBServiceError(Exception):
    """Raised when a TMDB request fails (network error, bad status, or
    missing configuration). Routers catch this and translate it into a
    clean HTTPException with an appropriate status code."""

    def __init__(self, message: str, status_code: int = 502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


async def _get(endpoint: str, params: Optional[dict] = None) -> dict:
    """
    Low-level GET helper for any TMDB endpoint. Injects the API key and
    default language, and converts network/HTTP failures into a
    TMDBServiceError so callers don't need to know about httpx internals.

    @param endpoint - TMDB path, e.g. "/movie/popular" or "/discover/movie"
    @param params - extra query params (genre filters, language, etc.)
    """
    
    if not settings.TMDB_API_KEY:
        raise TMDBServiceError(
            "TMDB_API_KEY is not configured on the server.", status_code=500
        )

    query = {
        "api_key": settings.TMDB_API_KEY,
        "language": settings.TMDB_DEFAULT_LANGUAGE,
    }
    if params:
        query.update(params)

    url = f"{settings.TMDB_BASE_URL}{endpoint}"

    async with _request_semaphore:
        for attempt in range(3):
            try:
                response = await _client.get(url, params=query)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as exc:
                raise TMDBServiceError(
                    f"TMDB request failed with status {exc.response.status_code}",
                    status_code=exc.response.status_code,
                ) from exc
            except httpx.RequestError as exc:
                if attempt < 2:
                    await asyncio.sleep(0.25)
                    continue

                detail = str(exc) or exc.__class__.__name__
                raise TMDBServiceError(
                    f"Could not reach TMDB: {detail}", status_code=503
                ) from exc


async def close_client() -> None:
    """Release the pooled TMDB connection when FastAPI shuts down."""
    await _client.aclose()


async def _discover_movies(params: dict) -> list:
    """Shared helper for any request that goes through /discover/movie."""
    data = await _get("/discover/movie", params)
    return data.get("results", [])


async def get_trending_movies(extra_params: Optional[dict] = None) -> list:
    """
    Trending movies (this week). If extra_params is given (e.g. a genre or
    provider filter), falls back to /discover/movie with a popularity sort,
    since TMDB's dedicated /trending endpoint doesn't accept discover-style
    filters.
    """
    if extra_params:
        params = {"sort_by": "popularity.desc", **extra_params}
        return await _discover_movies(params)

    data = await _get("/trending/movie/week")
    return data.get("results", [])


async def get_popular_movies(extra_params: Optional[dict] = None) -> list:
    """
    Popular movies. Same fallback pattern as get_trending_movies: TMDB's
    /movie/popular doesn't accept extra filters, so filtered requests go
    through /discover/movie instead.
    """
    if extra_params:
        params = {"sort_by": "popularity.desc", **extra_params}
        return await _discover_movies(params)

    data = await _get("/movie/popular")
    return data.get("results", [])


async def get_top_rated_movies(extra_params: Optional[dict] = None) -> list:
    """
    Top rated movies. vote_count.gte=200 mirrors the quality bar TMDB's own
    /movie/top_rated applies, so filtered results stay meaningfully "top rated"
    rather than a single 10/10 vote from one person.
    """
    if extra_params:
        params = {"sort_by": "vote_average.desc", "vote_count.gte": 200, **extra_params}
        return await _discover_movies(params)

    data = await _get("/movie/top_rated")
    return data.get("results", [])


async def get_movies_by_genre(genre_id: int, extra_params: Optional[dict] = None) -> list:
    """Movies in a given genre, optionally combined with other filters
    (language, watch provider, etc.) via extra_params."""
    params = {"with_genres": genre_id}
    if extra_params:
        params.update(extra_params)
    return await _discover_movies(params)


async def get_movies_by_language(language_code: str, extra_params: Optional[dict] = None) -> list:
    """Movies whose original_language matches language_code, optionally
    combined with other filters (genre, etc.) via extra_params."""
    params = {"with_original_language": language_code, "include_adult": "false"}
    if extra_params:
        params.update(extra_params)
    return await _discover_movies(params)


async def get_movies_by_ott(
    provider_id: int,
    watch_region: Optional[str] = None,
    extra_params: Optional[dict] = None,
) -> list:
    """Movies available on a given OTT platform in watch_region, optionally
    combined with other filters (genre, etc.) via extra_params."""
    region = watch_region or settings.DEFAULT_WATCH_REGION
    params = {
        "with_watch_providers": provider_id,
        "watch_region": region,
        "include_adult": "false",
    }
    if extra_params:
        params.update(extra_params)
    return await _discover_movies(params)


async def get_movie_details(movie_id: int) -> dict:
    """Fetch the movie detail shape used by the recommendation page."""
    data = await _get(f"/movie/{movie_id}")
    return {
        "id": data["id"],
        "title": data.get("title"),
        "poster_path": data.get("poster_path"),
        "backdrop_path": data.get("backdrop_path"),
        "overview": data.get("overview"),
        "release_date": data.get("release_date"),
        "vote_average": data.get("vote_average"),
        "genre_ids": [genre["id"] for genre in data.get("genres", [])],
    }
