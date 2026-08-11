from app.services.mesh_llm_service import (
    mesh_llm_service
)
import json

class RecommendationGenerationService:

    def generate(
        self,
        ranked_products,
        behavior_summary,
    ):
        if not ranked_products:
            return None

        products_text = ""

        for item in ranked_products:
            product = item["product"]

            products_text += f"""
Product ID:
{product.id}

Product Title:
{product.title}

Category:
{product.category}

Difficulty:
{product.difficulty}

Score:
{item["final_score"]}

Semantic Match:
{item["semantic_score"]}

Preference Match:
{item["preference_score"]}
"""

        system_prompt = """
You are SmartReco,
an AI learning recommendation assistant.

Your task is to select the best learning product
from the products provided.

Rules:

1. Recommend ONLY a product from the provided list.
2. Do not invent product details or change product IDs.
3. Use the behavioral information and ranking scores.
4. Explain why the selected product matches the user.
5. Return ONLY valid JSON.
6. Do not use markdown.
7. Do not include ```json.
8. The JSON must follow exactly this structure:

{
    "product_id": integer,
    "title": string,
    "reason": string,
    "confidence": number
}

confidence must be between 0 and 1.
"""

        user_prompt = f"""
User behavior:

{behavior_summary}

Available products:

{products_text}

Select the single best recommendation.

Return ONLY the required JSON object.
"""

        response = mesh_llm_service.generate(
            system_prompt,
            user_prompt,
        )

        try:
            recommendation = json.loads(response)
        except json.JSONDecodeError:
            raise ValueError(
                f"LLM returned invalid JSON: {response}"
            )

        # Enforce exact database product_id from the top-ranked product if missing or wrong
        top_product = ranked_products[0]["product"]
        if recommendation.get("product_id") != top_product.id:
            recommendation["product_id"] = top_product.id
            if not recommendation.get("title"):
                recommendation["title"] = top_product.title

        return recommendation


recommendation_generation_service = (
    RecommendationGenerationService()
)