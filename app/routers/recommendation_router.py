from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.repositories.product_repository import product_repository

# 1. Import the Agent or Hybrid Ranking Service instead of legacy pre-calculated service
from app.agents.recommendation_agent_v2 import recommendation_agent_v2  # or your agent invocation helper
from app.services.recommendation_service import recommendation_service


router = APIRouter(
    prefix="/recommendations",
    tags=["Recommendations"],
)

templates = Jinja2Templates(
    directory="app/templates"
)

@router.get("", response_class=HTMLResponse)
def recommendation_page(
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    ai_pick_item = None
    hybrid_ranked_items = []

    try:
        agent_input = {"user_id": current_user.id, "limit": 5}
        agent_response = recommendation_agent_v2.invoke(agent_input)

        # 1. Extract Top AI Pick from LLM node
        ai_rec = agent_response.get("ai_recommendation")
        if ai_rec and isinstance(ai_rec, dict):
            pid = ai_rec.get("product_id")
            if pid:
                product = product_repository.get_by_id(db, pid)
                if product:
                    ai_pick_item = {
                        "product": product,
                        "recommendation": ai_rec,
                        "reason": ai_rec.get("reason", ""),
                        "confidence": ai_rec.get("confidence", 0.0),
                    }

        # 2. Extract ranked recommendations from hybrid_rank node
        raw_ranked = agent_response.get("ranked_recommendations", [])

        for idx, item in enumerate(raw_ranked, start=1):
            item_dict = dict(item) if isinstance(item, dict) else item.__dict__

            # The SQLAlchemy Product model object is already in item_dict['product']
            product = item_dict.get("product")

            # Fallback DB lookup if only product_id is stored
            if not product or not hasattr(product, "title"):
                pid = item_dict.get("product_id")
                if pid:
                    product = product_repository.get_by_id(db, pid)

            if product:
                hybrid_ranked_items.append(
                    {
                        "product": product,
                        "recommendation": item_dict,
                        "rank": idx,
                    }
                )

    except Exception as e:
        print(f"Error executing recommendation agent: {e}")

    return templates.TemplateResponse(
        request=request,
        name="recommendations/index.html",
        context={
            "request": request,
            "ai_pick": ai_pick_item,
            "hybrid_recommendations": hybrid_ranked_items,
        },
    )