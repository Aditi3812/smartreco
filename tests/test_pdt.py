from app.schemas.product import ProductCreate

product = ProductCreate(
    title="AI Agents",
    description="Learn Agentic AI",
    category="AI",
    difficulty="Advanced",
    language="English",
    duration=18,
    price=999,
    instructor="John",
    skills="Python,RAG",
    tags="AI,LLM",
)

print(product)