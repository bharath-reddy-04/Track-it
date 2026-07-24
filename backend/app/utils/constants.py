"""
constants.py
------------
Static lookup tables used across services/routers. Centralizing these here
means genre and provider IDs are defined exactly once in the whole backend.
"""

# TMDB's official genre IDs for movies.
GENRE_IDS = {
    "action": 28,
    "comedy": 35,
    "horror": 27,
    "romance": 10749,
    "animation": 16,
}

# TMDB watch-provider IDs, keyed by the URL-friendly slug the frontend sends
# in GET /api/ott/{provider}.
#
# NOTE on jiohotstar: JioHotstar is the 2025 merger/rebrand of Disney+ Hotstar
# and JioCinema in India. As of this writing, TMDB has not published a
# separate provider ID for it — it appears under the existing Disney+ Hotstar
# provider record (id 122). If TMDB later splits these into distinct IDs,
# update the value below by checking:
#   GET https://api.themoviedb.org/3/watch/providers/movie?watch_region=IN
OTT_PROVIDER_IDS = {
    "netflix": 8,
    "amazon-prime-video": 9,
    "disney-hotstar": 122,
    "zee5": 232,
    "sonyliv": 237,
    "jiohotstar": 122,  # see NOTE above
    "apple-tv-plus": 350,
    "hulu": 15,
    "max": 1899,
    "paramount-plus": 531,
    "peacock": 386,
    "crunchyroll": 283,
}