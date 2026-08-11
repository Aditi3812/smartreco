from sqlalchemy.orm import Session

from app.models.behavior_profile import BehaviorProfile


class BehaviorProfileRepository:
    """
    Handles database operations
    for behavioral profiles.
    """

    def get_by_user_id(
        self,
        db: Session,
        user_id: int,
    ):
        return (
            db.query(BehaviorProfile)
            .filter(
                BehaviorProfile.user_id == user_id
            )
            .first()
        )

    def create(
        self,
        db: Session,
        user_id: int,
    ):

        profile = BehaviorProfile(
            user_id=user_id,
            category_scores={},
            difficulty_scores={},
            language_scores={},
            search_frequency=0,
            average_time_spent=0,
            average_scroll_depth=0,
            purchase_intent=0,
            total_events=0,
        )

        db.add(profile)
        db.flush()
        db.refresh(profile)

        return profile

    def get_or_create(
        self,
        db: Session,
        user_id: int,
    ):

        profile = self.get_by_user_id(
            db,
            user_id,
        )

        if profile:
            return profile

        return self.create(
            db,
            user_id,
        )

    def update(
        self,
        db: Session,
        profile: BehaviorProfile,
    ):
        db.flush()
        db.refresh(profile)

        return profile


behavior_profile_repository = (
    BehaviorProfileRepository()
)