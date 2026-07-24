from fastapi import APIRouter, HTTPException, status

from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    MovieClickRequest,
    MovieClickResponse,
)
from app.services import customer_service

router = APIRouter(prefix="/api/customer", tags=["customer"])


@router.post(
    "/create",
    response_model=CustomerResponse,
    status_code=status.HTTP_200_OK,
    summary="Create a new customer, or return the existing one for that email",
)
async def create_customer(payload: CustomerCreate):
    try:
        customer = customer_service.create_customer(payload)
        return customer
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create customer: {exc}",
        )


@router.post(
    "/movie",
    response_model=MovieClickResponse,
    status_code=status.HTTP_200_OK,
    summary="Record a movie click for a customer",
)
async def track_movie_click(payload: MovieClickRequest):
    try:
        customer_service.update_clicked_movie(str(payload.customer_id), payload.movie)
        return {"success": True}
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update movie: {exc}",
        )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
    summary="Fetch a customer by id",
)

async def get_customer(customer_id: str):
    customer = customer_service.get_customer(customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return customer
