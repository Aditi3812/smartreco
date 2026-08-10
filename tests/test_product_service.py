from app.database.database import SessionLocal
from app.schemas.product import ProductCreate
from app.services.product_service import product_service

db = SessionLocal()

product = ProductCreate(
    title="LangChain Masterclass",
    description="Production AI Systems",
    category="AI",
    difficulty="Intermediate",
    language="English",
    duration=12,
    price=999,
    instructor="OpenAI",
    skills="Python,RAG,LangChain",
    tags="AI,LLM",
)

created = product_service.create_product(
    db,
    product,
)

print(created.id)
print(created.title)

db.close()