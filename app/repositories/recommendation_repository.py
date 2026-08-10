from sqlalchemy.orm import Session

from app.models.recommendation import Recommendation


class RecommendationRepository:
    """
    Handles database operations
    related to recommendations.
    """

    def create(
        self,
        db: Session,
        recommendation: Recommendation,
    ) -> Recommendation:

        db.add(recommendation)
        db.commit()
        db.refresh(recommendation)

        return recommendation

    def get_by_id(
        self,
        db: Session,
        recommendation_id: int,
    ) -> Recommendation | None:

        return (
            db.query(Recommendation)
            .filter(
                Recommendation.id == recommendation_id
            )
            .first()
        )

    def get_by_user(
        self,
        db: Session,
        user_id: int,
    ) -> list[Recommendation]:

        return (
            db.query(Recommendation)
            .filter(
                Recommendation.user_id == user_id
            )
            .order_by(
                Recommendation.created_at.desc()
            )
            .all()
        )

    def get_latest_for_user(
        self,
        db: Session,
        user_id: int,
        limit: int = 5,
    ) -> list[Recommendation]:

        return (
            db.query(Recommendation)
            .filter(
                Recommendation.user_id == user_id
            )
            .order_by(
                Recommendation.created_at.desc()
            )
            .limit(limit)
            .all()
        )

    def delete(
        self,
        db: Session,
        recommendation: Recommendation,
    ) -> None:

        db.delete(recommendation)
        db.commit()


recommendation_repository = RecommendationRepository()