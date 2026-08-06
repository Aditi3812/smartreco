from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str
    category: str
    difficulty: str
    language: str = "English"
    duration: int
    price: float = 0
    instructor: str
    skills: str
    tags: str


class ProductUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    category: str | None = None
    difficulty: str | None = None
    language: str | None = None
    duration: int | None = None
    price: float | None = None
    instructor: str | None = None
    skills: str | None = None
    tags: str | None = None


class ProductResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    difficulty: str
    language: str
    duration: int
    price: float
    instructor: str
    skills: str
    tags: str
    embedding_generated: bool

    model_config = ConfigDict(from_attributes=True)