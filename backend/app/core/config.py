"""
config.py
---------
Central place for environment-driven configuration. Everything else in the
app (services, routers) reads settings from here instead of calling
os.getenv() directly, so there is exactly one place that knows about env
var names and defaults.
"""

import os
from dotenv import load_dotenv

# Loads variables from backend/.env into the process environment.
# Safe to call even if .env doesn't exist (falls back to real env vars).
load_dotenv()

class Settings:
    # TMDB
    TMDB_API_KEY: str = os.getenv("TMDB_API_KEY")
    TMDB_BASE_URL: str = "https://api.themoviedb.org/3"
    TMDB_DEFAULT_LANGUAGE: str = os.getenv("TMDB_DEFAULT_LANGUAGE", "en-US")

    # Watch-provider filtering is region-specific on TMDB; this is the
    # default region used for every OTT-provider request unless overridden.
    DEFAULT_WATCH_REGION: str = os.getenv("DEFAULT_WATCH_REGION", "IN")

    # CORS — comma-separated list of origins allowed to call this API.
    # Defaults to the React dev server.
    CORS_ORIGINS: list = [
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
        if origin.strip()
    ]

    # Outbound HTTP timeout (seconds) for every TMDB request.
    TMDB_TIMEOUT_SECONDS: float = float(os.getenv("TMDB_TIMEOUT_SECONDS", "10"))

    # /api/home fetches several TMDB rows concurrently. Keeping this below the
    # number of rows prevents a burst of TLS connections from overwhelming a
    # restrictive network or proxy.
    TMDB_MAX_CONCURRENT_REQUESTS: int = int(
        os.getenv("TMDB_MAX_CONCURRENT_REQUESTS", "1")
    )


# Singleton settings instance imported throughout the app.
settings = Settings()
