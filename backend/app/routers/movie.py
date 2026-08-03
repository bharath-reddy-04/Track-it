"""Movie routes that serve UI-specific movie information."""

from fastapi import APIRouter, HTTPException

from app.schemas.movie import WatchProvidersResponse
from app.services import movie_service
from app.services.tmdb_service import TMDBServiceError

router = APIRouter(prefix="/api/movie", tags=["movies"])


@router.get("/{movie_id}/watch-providers", response_model=WatchProvidersResponse)
async def get_movie_watch_providers(movie_id: int):
    """Return subscription streaming providers available in India for a movie."""
    try:
        return await movie_service.get_watch_providers(movie_id)
    except TMDBServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
