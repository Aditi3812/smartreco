from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.auth.dependencies import (
    get_current_user,
)
from app.database.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
)
from fastapi.templating import Jinja2Templates
from app.services.product_service import product_service
from app.auth.permissions import require_admin
router = APIRouter(
    prefix="/products",
    tags=["Products"],
)
templates = Jinja2Templates(
    directory="app/templates"
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
    response_class=HTMLResponse,
)
def product_catalog(
    request: Request,
    db: Session = Depends(get_db),
    q: str = Query(default=""),
):

    products = product_service.search_products(
        db,
        q,
    )

    return templates.TemplateResponse(
        request=request,
        name="products/catalog.html",
        context={
            "products": products,
            "request": request,
            "query": q,
        },
    )
@router.get(
    "/{product_id}",
    response_class=HTMLResponse,
)
def product_detail(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db),
):

    product = product_service.get_product(
        db,
        product_id,
    )

    if product is None:
        raise HTTPException(
            status_code=404,
            detail="Product not found",
        )

    return templates.TemplateResponse(
        request=request,
        name="products/detail.html",
        context={
            "product": product,
        },
    )

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
