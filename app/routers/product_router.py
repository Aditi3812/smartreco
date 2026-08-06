from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    get_current_user,
    require_admin,
)
from app.database.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
)
from app.services.product_service import product_service

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)
@router.post(
    "",
    response_model=ProductResponse,
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    try:
        return product_service.create_product(
            db,
            product,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_products(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return product_service.get_all_products(
        db,
    )
@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    product = product_service.get_product(
        db,
        product_id,
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return product
@router.delete(
    "/{product_id}",
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    try:
        product_service.delete_product(
            db,
            product_id,
        )

        return {
            "message": "Product deleted successfully."
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )