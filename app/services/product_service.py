from sqlalchemy.orm import Session

from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate


class ProductService:
    """
    Handles business logic
    related to products.
    """

    def __init__(self):
        self.product_repository = ProductRepository()

    def create_product(
        self,
        db: Session,
        product: ProductCreate,
    ):

        # ---------- Validation ----------

        if product.price < 0:
            raise ValueError(
                "Price cannot be negative."
            )

        if product.duration <= 0:
            raise ValueError(
                "Duration must be greater than zero."
            )

        # ---------- Duplicate Check ----------

        existing = self.product_repository.get_by_title(
            db,
            product.title,
        )

        if existing:
            raise ValueError(
                "Product already exists."
            )

        # ---------- Save ----------

        created_product = (
            self.product_repository.create_product(
                db,
                product,
            )
        )

        return created_product

    def get_product(
        self,
        db: Session,
        product_id: int,
    ):
        return self.product_repository.get_by_id(
            db,
            product_id,
        )

    def get_all_products(
    self,
    db: Session,
    page: int = 1,
    limit: int = 100,
):

        skip = (page - 1) * limit


        products = (
            self.product_repository
            .get_all_products(
                db,
                skip,
                limit,
            )
        )


        total = (
            self.product_repository
            .count_products(db)
        )


        pages = (total + limit - 1) // limit


        return {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
            "items": products,
        }

    def get_products_by_category(
        self,
        db: Session,
        category: str,
    ):
        return self.product_repository.get_by_category(
            db,
            category,
        )

    def delete_product(
        self,
        db: Session,
        product_id: int,
    ):

        product = self.product_repository.get_by_id(
            db,
            product_id,
        )

        if not product:
            raise ValueError(
                "Product not found."
            )

        self.product_repository.delete_product(
            db,
            product,
        )
    def search_products(
        self,
        db: Session,
        query: str = "",
        page: int = 1,
        limit: int = 10,
        category: str | None = None,
        difficulty: str | None = None,
        language: str | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        min_duration: int | None = None,
        max_duration: int | None = None,
    ):

            skip = (page - 1) * limit

            products = self.product_repository.search_products(
                db,
                query,
                category,
                difficulty,
                language,
                min_price,
                max_price,
                min_duration,
                max_duration,
                skip,
                limit,
            )

            total = self.product_repository.count_search_products(
                db,
                query,
                category,
                difficulty,
                language,
                min_price,
                max_price,
                min_duration,
                max_duration,
            )

            pages = (total + limit - 1) // limit

            return {
                "items": products,
                "page": page,
                "limit": limit,
                "total": total,
                "pages": pages,
            }

product_service = ProductService()