from app.database.database import SessionLocal
from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate

db = SessionLocal()

repo = ProductRepository()

product = ProductCreate(
    title="LangGraph Masterclass",
    description="Complete production LangGraph course",
    category="AI",
    difficulty="Advanced",
    language="English",
    duration=20,
    price=999,
    instructor="OpenAI",
    skills="Python,LangGraph,RAG",
    tags="AI,Agents,LLM",
)

created = repo.create_product(db, product)

print(created.id)
print(created.title)
print(created.category)

db.close()