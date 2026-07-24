"""
main.py
-------
FastAPI application entrypoint. Wires up CORS and every router.

Run with:
    uvicorn app.main:app --reload
(from inside the backend/ directory)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import customer, genre, home, language, ott, recommendation
from app.services import tmdb_service

app = FastAPI(
    title="Movie Recommendation API",
    description="Backend that proxies and aggregates TMDB movie data for the React frontend. "
    "The frontend never calls TMDB directly — every request goes through here.",
    version="1.0.0",
)

# Allow the React dev server (and any other configured origins) to call this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(home.router)
app.include_router(language.router)
app.include_router(genre.router)
app.include_router(ott.router)
app.include_router(customer.router)
app.include_router(recommendation.router)


@app.on_event("shutdown")
async def close_tmdb_client():
    await tmdb_service.close_client()


@app.get("/", tags=["health"])
async def root():
    """Simple health check / landing endpoint."""
    return {"status": "ok", "service": "movie-recommendation-backend"}
