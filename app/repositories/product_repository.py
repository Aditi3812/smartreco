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
    ):

        return db.query(Product).all()

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