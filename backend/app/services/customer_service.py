"""
Service layer for all customer-related Supabase operations.
Keep all database logic here — routers should never talk to Supabase directly.
"""

from datetime import datetime, timezone
from typing import Optional

from database.supabase import supabase
from app.schemas.customer import CustomerCreate, Movie

TABLE = "customer"


def get_customer_by_email(email: str) -> Optional[dict]:
    """Return the customer row matching the given email, or None."""
    response = supabase.table(TABLE).select("*").eq("email", email).limit(1).execute()
    data = response.data
    return data[0] if data else None


def get_customer(customer_id: str) -> Optional[dict]:
    """Return the customer row matching the given id, or None."""
    response = supabase.table(TABLE).select("*").eq("id", customer_id).limit(1).execute()
    data = response.data
    return data[0] if data else None


def create_customer(payload: CustomerCreate) -> dict:
    """
    Create a new customer, or return the existing one if the email
    is already registered (idempotent "get or create").
    """
    existing = get_customer_by_email(payload.email)
    if existing:
        return existing

    now = datetime.now(timezone.utc).isoformat()
    insert_data = {
        "name": payload.name,
        "email": payload.email,
        "movies": [],
        "created_at": now,
        "updated_at": now,
    }

    response = supabase.table(TABLE).insert(insert_data).execute()
    if not response.data:
        raise RuntimeError("Failed to create customer")
    return response.data[0]


def movie_exists(movies: list, movie_id: int) -> Optional[int]:
    """Return the index of the movie with the given id in the movies list, or None."""
    for index, m in enumerate(movies):
        if m.get("id") == movie_id:
            return index
    return None


def update_clicked_movie(customer_id: str, movie: Movie) -> dict:
    """
    Append the clicked movie to the customer's movies array, or update
    clicked_at if it's already present. Avoids duplicate entries.
    """
    customer = get_customer(customer_id)
    if not customer:
        raise ValueError("Customer not found")

    movies = customer.get("movies") or []
    clicked_at = datetime.now(timezone.utc).isoformat()

    existing_index = movie_exists(movies, movie.id)

    if existing_index is not None:
        movies[existing_index]["clicked_at"] = clicked_at
    else:
        movie_dict = movie.model_dump(exclude={"clicked_at"})
        movie_dict["clicked_at"] = clicked_at
        movies.append(movie_dict)

    update_data = {
        "movies": movies,
        "updated_at": clicked_at,
    }

    response = (
        supabase.table(TABLE)
        .update(update_data)
        .eq("id", customer_id)
        .execute()
    )
    if not response.data:
        raise RuntimeError("Failed to update customer movies")
    return response.data[0]
