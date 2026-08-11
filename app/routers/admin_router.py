from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.permissions import require_admin
from app.database.database import get_db
from app.schemas.product import ProductCreate
from app.services.product_service import product_service

router = APIRouter(prefix="/admin", tags=["Admin"])

templates = Jinja2Templates(directory="app/templates")

@router.get(
    "/products",
    response_class=HTMLResponse,
)
def admin_products(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    product_data = product_service.get_all_products(
        db,
        page=1,
        limit=100,
    )

    # Extract items array from the response dict
    if isinstance(product_data, dict):
        products_list = product_data.get("items", [])
    else:
        products_list = product_data

    return templates.TemplateResponse(
        request=request,
        name="admin/products.html",
        context={
            "request": request,
            "products": products_list,
            "user": user,
        },
    )


@router.get(
    "/dashboard",
    response_class=HTMLResponse,
)
def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    product_data = product_service.get_all_products(
        db,
        page=1,
        limit=10,
    )

    if isinstance(product_data, dict):
        products_list = product_data.get("items", [])
    else:
        products_list = product_data

    return templates.TemplateResponse(
        request=request,
        name="admin/dashboard.html",
        context={
            "request": request,
            "products": products_list,
            "user": user,
        },
    )
@router.post("/products/create")
def create_product_admin(
    title: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    difficulty: str = Form(...),
    language: str = Form(...),
    duration: int = Form(...),
    price: float = Form(...),
    instructor: str = Form(...),
    skills: str = Form(...),
    tags: str = Form(...),
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    product = ProductCreate(
        title=title,
        description=description,
        category=category,
        difficulty=difficulty,
        language=language,
        duration=duration,
        price=price,
        instructor=instructor,
        skills=skills,
        tags=tags,
    )
    product_service.create_product(
        db,
        product,
    )
    return RedirectResponse(
        "/admin/products",
        status_code=303,
    )


@router.get("/products/delete/{product_id}")
def delete_product_admin(
    product_id: int,
    db: Session = Depends(get_db),
    user=Depends(require_admin),
):
    product_service.delete_product(
        db,
        product_id,
    )
    return RedirectResponse(
        "/admin/products",
        status_code=303,
    )