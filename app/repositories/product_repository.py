from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


class ProductRepository:
    """
    Handles all database operations
    related to products.
    """

    def create_product(
        self,
        db: Session,
        product: ProductCreate,
    ) -> Product:

        new_product = Product(
            title=product.title,
            description=product.description,
            category=product.category,
            difficulty=product.difficulty,
            language=product.language,
            duration=product.duration,
            price=product.price,
            instructor=product.instructor,
            skills=product.skills,
            tags=product.tags,
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product

    def get_by_id(
        self,
        db: Session,
        product_id: int,
    ) -> Product | None:

        return (
            db.query(Product)
            .filter(Product.id == product_id)
            .first()
        )

    def get_all_products(
    self,
    db: Session,
    skip: int = 0,
    limit: int = 10,
):

        return (
            db.query(Product)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_all(
    self,
    db: Session,
):
        return (
            db.query(Product)
            .all()
        )
    
    def count_search_products(
    self,
    db: Session,
    query: str = "",
    category: str | None = None,
    difficulty: str | None = None,
    language: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_duration: int | None = None,
    max_duration: int | None = None,
):

        products_query = db.query(Product)

        if query:
            products_query = products_query.filter(
                Product.title.ilike(f"%{query}%")
            )

        if category:
            products_query = products_query.filter(
                Product.category == category
            )

        if difficulty:
            products_query = products_query.filter(
                Product.difficulty == difficulty
            )

        if language:
            products_query = products_query.filter(
                Product.language == language
            )

        if min_price is not None:
            products_query = products_query.filter(
                Product.price >= min_price
            )

        if max_price is not None:
            products_query = products_query.filter(
                Product.price <= max_price
            )

        if min_duration is not None:
            products_query = products_query.filter(
                Product.duration >= min_duration
            )

        if max_duration is not None:
            products_query = products_query.filter(
                Product.duration <= max_duration
            )

        return products_query.count()
    
    def get_by_category(
        self,
        db: Session,
        category: str,
    ):

        return (
            db.query(Product)
            .filter(Product.category == category)
            .all()
        )

    def update_product(
        self,
        db: Session,
        product: Product,
    ):

        db.commit()
        db.refresh(product)

        return product

    def delete_product(
        self,
        db: Session,
        product: Product,
    ):

        db.delete(product)
        db.commit()

    def get_by_title(
        self,
        db: Session,
        title: str,
    ):
        return (
            db.query(Product)
            .filter(Product.title == title)
            .first()
        )
    def search_products(
    self,
    db: Session,
    query: str = "",
    category: str | None = None,
    difficulty: str | None = None,
    language: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_duration: int | None = None,
    max_duration: int | None = None,
    skip: int = 0,
    limit: int = 10,
):

        products_query = db.query(Product)

        # Search
        if query:
            products_query = products_query.filter(
                Product.title.ilike(f"%{query}%")
            )

        # Category
        if category:
            products_query = products_query.filter(
                Product.category == category
            )

        # Difficulty
        if difficulty:
            products_query = products_query.filter(
                Product.difficulty == difficulty
            )

        # Language
        if language:
            products_query = products_query.filter(
                Product.language == language
            )

        # Price
        if min_price is not None:
            products_query = products_query.filter(
                Product.price >= min_price
            )

        if max_price is not None:
            products_query = products_query.filter(
                Product.price <= max_price
            )

        # Duration
        if min_duration is not None:
            products_query = products_query.filter(
                Product.duration >= min_duration
            )

        if max_duration is not None:
            products_query = products_query.filter(
                Product.duration <= max_duration
            )

        return (
            products_query
            .offset(skip)
            .limit(limit)
            .all()
        )
    def count_products(
    self,
    db: Session,
):
        return (
            db.query(Product)
            .count()
        )
product_repository = ProductRepository()