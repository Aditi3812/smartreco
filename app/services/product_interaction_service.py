
import json
import math
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.repositories.event_repository import event_repository
from app.repositories.product_interaction_repository import (
    product_interaction_repository,
)


class ProductInteractionService:
    """
    Converts product-related events into
    per-user product interaction memory.
    """

    def __init__(self):
        self.event_repository = event_repository
        self.interaction_repository = (
            product_interaction_repository
        )

    def build_interactions(
        self,
        db: Session,
        user_id: int,
    ):
        # --------------------------------
        # Get all user events
        # --------------------------------

        events = (
            self.event_repository.get_by_user_id(
                db,
                user_id,
            )
        )

        # --------------------------------
        # Delete old interaction records
        # --------------------------------

        existing = (
            self.interaction_repository.get_by_user(
                db,
                user_id,
            )
        )

        for interaction in existing:
            db.delete(interaction)

        db.commit()

        # --------------------------------
        # Rebuild from events
        # --------------------------------

        interactions = {}

        for event in events:

            if not event.product_id:
                continue

            product_id = event.product_id

            # --------------------------------
            # Create in-memory interaction
            # --------------------------------

            if product_id not in interactions:

                interactions[product_id] = {
                    "view_count": 0,
                    "total_time_spent": 0,
                    "max_scroll_depth": 0,
                    "search_count": 0,
                    "last_interacted_at": None,
                }

            interaction = interactions[product_id]
            if (
                interaction["last_interacted_at"] is None
                or event.created_at
                > interaction["last_interacted_at"]
            ):
                interaction["last_interacted_at"] = (
                    event.created_at
                )
            # --------------------------------
            # PRODUCT VIEW
            # --------------------------------

            if event.event_type == "PRODUCT_VIEW":

                interaction["view_count"] += 1

            # --------------------------------
            # TIME SPENT
            # --------------------------------

            elif event.event_type == "TIME_SPENT":

                metadata = self._parse_metadata(
                    event.event_metadata
                )

                seconds = metadata.get(
                    "seconds",
                    0,
                )

                interaction[
                    "total_time_spent"
                ] += float(seconds)

            # --------------------------------
            # SCROLL DEPTH
            # --------------------------------

            elif event.event_type == "SCROLL_DEPTH":

                metadata = self._parse_metadata(
                    event.event_metadata
                )

                depth = metadata.get(
                    "depth",
                    0,
                )

                interaction[
                    "max_scroll_depth"
                ] = max(
                    interaction[
                        "max_scroll_depth"
                    ],
                    float(depth),
                )

            # --------------------------------
            # SEARCH
            # --------------------------------

            elif event.event_type == "SEARCH":

                interaction[
                    "search_count"
                ] += 1

        # --------------------------------
        # Persist rebuilt interactions
        # --------------------------------

        results = []

        for product_id, data in interactions.items():

            interaction = (
                self.interaction_repository.create(
                    db,
                    user_id,
                    product_id,
                )
            )

            # --------------------------------
            # Store aggregated values
            # --------------------------------

            interaction.view_count = (
                data["view_count"]
            )

            interaction.total_time_spent = (
                data["total_time_spent"]
            )

            interaction.max_scroll_depth = (
                data["max_scroll_depth"]
            )

            interaction.search_count = (
                data["search_count"]
            )
            interaction.last_interacted_at = (
                data["last_interacted_at"]
            )
            # --------------------------------
            # Calculate interaction score
            # --------------------------------

            interaction.interaction_score = (
                self.calculate_interaction_score(
                    interaction
                )
            )
            interaction.recency_score = (
                self.calculate_recency_score(
                    interaction
                )
            )
            interaction.final_score = round(
                interaction.interaction_score
                * interaction.recency_score,
                4,
            )
            # --------------------------------
            # Save
            # --------------------------------

            db.commit()
            db.refresh(interaction)

            results.append(interaction)

        return results
    def calculate_recency_score(
        self,
        interaction,
    ) -> float:

        if not interaction.last_interacted_at:
            return 1.0

        now = datetime.now(timezone.utc)

        last_interaction = (
            interaction.last_interacted_at
        )

        age_seconds = (
            now - last_interaction
        ).total_seconds()

        age_days = (
            age_seconds / 86400
        )

        decay_rate = 0.1

        recency = math.exp(
            -decay_rate * age_days
        )

        return round(
            recency,
            4,
        )
    # ------------------------------------
    # Metadata helper
    # ------------------------------------

    def _parse_metadata(
        self,
        metadata,
    ):

        if not metadata:
            return {}

        if isinstance(
            metadata,
            dict,
        ):
            return metadata

        if isinstance(
            metadata,
            str,
        ):

            try:

                return json.loads(
                    metadata
                )

            except json.JSONDecodeError:

                return {}

        return {}

    # ------------------------------------
    # Interaction Score
    # ------------------------------------

    def calculate_interaction_score(
        self,
        interaction,
    ) -> float:

        MAX_VIEWS = 20
        MAX_TIME = 300
        MAX_SEARCHES = 5

        # --------------------------------
        # View Score
        # --------------------------------

        view_score = (
            math.log1p(
                interaction.view_count
            )
            / math.log1p(
                MAX_VIEWS
            )
        )

        view_score = min(
            view_score,
            1.0,
        )

        # --------------------------------
        # Time Score
        # --------------------------------

        time_score = min(
            interaction.total_time_spent
            / MAX_TIME,
            1.0,
        )

        # --------------------------------
        # Scroll Score
        # --------------------------------

        scroll_score = min(
            interaction.max_scroll_depth
            / 100,
            1.0,
        )

        # --------------------------------
        # Search Score
        # --------------------------------

        search_score = min(
            interaction.search_count
            / MAX_SEARCHES,
            1.0,
        )

        # --------------------------------
        # Final Score
        # --------------------------------

        score = (
            0.30 * view_score
            + 0.30 * time_score
            + 0.25 * scroll_score
            + 0.15 * search_score
        )

        return round(
            score,
            4,
        )
    def get_top_products(
        self,
        db: Session,
        user_id: int,
        limit: int = 10,
    ):
        return (
            self.interaction_repository.get_top_by_user(
                db,
                user_id,
                limit,
            )
        )


product_interaction_service = (
    ProductInteractionService()
)

