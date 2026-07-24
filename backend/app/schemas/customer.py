import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr


class Movie(BaseModel):
    id: int
    title: str
    poster_path: Optional[str] = None
    backdrop_path: Optional[str] = None
    release_date: Optional[str] = None
    vote_average: Optional[float] = None
    clicked_at: Optional[datetime] = None


class MovieClickRequest(BaseModel):
    customer_id: uuid.UUID
    movie: Movie


class CustomerResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr
    movies: List[dict] = []
    created_at: datetime
    updated_at: datetime


class MovieClickResponse(BaseModel):
    success: bool