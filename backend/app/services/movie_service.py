"""Movie-focused business logic built on top of the TMDB client."""

from collections.abc import Iterable

from app.core.config import settings
from app.services import tmdb_service


# Kept separate from the route so later support for rental/purchase/free
# providers only requires changing the requested categories, not the TMDB call.
SUBSCRIPTION_PROVIDER_TYPES = ("flatrate",)
UNAVAILABLE_MESSAGE = "This movie is currently not available on any OTT platform."


def _unique_providers(provider_groups: Iterable[list]) -> list[dict]:
    """Flatten TMDB provider groups while preserving TMDB's display order."""
    providers_by_id = {}
    for providers in provider_groups:
        for provider in providers or []:
            provider_id = provider.get("provider_id")
            if provider_id is not None:
                providers_by_id.setdefault(provider_id, provider)
    return list(providers_by_id.values())


async def get_watch_providers(
    movie_id: int,
    region: str | None = None,
    provider_types: tuple[str, ...] = SUBSCRIPTION_PROVIDER_TYPES,
) -> dict:
    """Return normalized providers for a movie in a selected TMDB region.

    The route currently uses India's default region and subscription services.
    ``region`` and ``provider_types`` keep this service ready for regional,
    rental, purchase, or ad-supported options without changing its interface.
    """
    watch_region = (region or settings.DEFAULT_WATCH_REGION).upper()
    data = await tmdb_service.get_movie_watch_provider_data(movie_id)
    regional_data = data.get("results", {}).get(watch_region, {})
    providers = _unique_providers(
        regional_data.get(provider_type, []) for provider_type in provider_types
    )

    if not providers:
        return {"available": False, "message": UNAVAILABLE_MESSAGE}

    return {
        "available": True,
        "providers": [
            {
                "provider_id": provider["provider_id"],
                "provider_name": provider["provider_name"],
                "logo_path": provider.get("logo_path"),
            }
            for provider in providers
        ],
        "link": regional_data.get("link", f"https://www.themoviedb.org/movie/{movie_id}/watch?locale={watch_region}"),
    }
