
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.repositories.product_repository import product_repository
from app.services.recommendation_service import recommendation_service


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)

templates = Jinja2Templates(
    directory="app/templates"
)


@router.get(
    "",
    response_class=HTMLResponse,
)
def recommendation_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    recommendations = (
        recommendation_service
        .get_latest_recommendations(
            db,
            current_user.id,
            limit=5,
        )
    )

    recommendation_items = []

    for recommendation in recommendations:

        product = (
            product_repository
            .get_by_id(
                db,
                recommendation.product_id,
            )
        )

        if not product:
            continue

        recommendation_items.append(
            {
                "recommendation": recommendation,
                "product": product,
            }
        )

    return templates.TemplateResponse(
        request=request,
        name="recommendations/index.html",
        context={
            "request": request,
            "recommendations": recommendation_items,
        },
    )

