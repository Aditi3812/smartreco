from sqlalchemy.orm import Session
from datetime import datetime, UTC
import math
from app.repositories.event_repository import event_repository
from app.repositories.behavior_profile_repository import (
    behavior_profile_repository,
)


class BehaviorProfileService:
    """
    Converts raw behavioral events
    into a user's behavioral profile.
    """

    def __init__(self):
        self.event_repository = event_repository
        self.profile_repository = behavior_profile_repository

    def build_profile(
        self,
        db: Session,
        user_id: int,
    ):

        # --------------------------------
        # Get user's events
        # --------------------------------

        events = self.event_repository.get_by_user_id(
            db,
            user_id,
        )

        # --------------------------------
        # Get or create profile
        # --------------------------------

        profile = self.profile_repository.get_or_create(
            db,
            user_id,
        )

        # --------------------------------
        # Counters
        # --------------------------------

        category_scores = {}
        difficulty_scores = {}
        language_scores = {}

        search_count = 0

        time_values = []
        scroll_values = []

        total_events = len(events)
        purchase_intent = (
            self.calculate_purchase_intent(
                events
            )
        )
        # --------------------------------
        # Process events
        # --------------------------------

        for event in events:

            # ==============================
            # PRODUCT VIEW
            # ==============================

            if event.event_type == "PRODUCT_VIEW":

                if event.category:

                    weight = self.calculate_recency_weight(
                        event
                    )

                    category_scores[event.category] = (
                        category_scores.get(
                            event.category,
                            0,
                        )
                        + weight
                    )

            # ==============================
            # SEARCH
            # ==============================

            elif event.event_type == "SEARCH":

                search_count += 1

            # ==============================
            # FILTER
            # ==============================

            elif event.event_type == "FILTER":

                if event.event_metadata:

                    metadata = (
                        event.event_metadata
                    )

                    if isinstance(
                        metadata,
                        str,
                    ):
                        import json

                        try:
                            metadata = json.loads(
                                metadata
                            )
                        except json.JSONDecodeError:
                            metadata = {}

                    difficulty = metadata.get(
                        "difficulty"
                    )

                    language = metadata.get(
                        "language"
                    )

                    if difficulty:

                        weight = self.calculate_recency_weight(
                            event
                        )

                        difficulty_scores[difficulty] = (
                            difficulty_scores.get(
                                difficulty,
                                0,
                            )
                            + weight
                        )

                    if language:

                        weight = self.calculate_recency_weight(
                            event
                        )

                        language_scores[language] = (
                            language_scores.get(
                                language,
                                0,
                            )
                            + weight
                        )

            # ==============================
            # TIME SPENT
            # ==============================

            elif event.event_type == "TIME_SPENT":

                if event.event_metadata:

                    metadata = (
                        event.event_metadata
                    )

                    if isinstance(
                        metadata,
                        str,
                    ):
                        import json

                        try:
                            metadata = json.loads(
                                metadata
                            )
                        except json.JSONDecodeError:
                            metadata = {}

                    seconds = metadata.get(
                        "seconds"
                    )

                    if seconds is not None:

                        time_values.append(
                            float(seconds)
                        )

            # ==============================
            # SCROLL DEPTH
            # ==============================

            elif event.event_type == "SCROLL_DEPTH":

                if event.event_metadata:

                    metadata = (
                        event.event_metadata
                    )

                    if isinstance(
                        metadata,
                        str,
                    ):
                        import json

                        try:
                            metadata = json.loads(
                                metadata
                            )
                        except json.JSONDecodeError:
                            metadata = {}

                    depth = metadata.get(
                        "depth"
                    )

                    if depth is not None:

                        scroll_values.append(
                            float(depth)
                        )

        # --------------------------------
        # Calculate averages
        # --------------------------------

        average_time = (
            sum(time_values)
            / len(time_values)
            if time_values
            else 0
        )

        average_scroll = (
            sum(scroll_values)
            / len(scroll_values)
            if scroll_values
            else 0
        )
        # --------------------------------
        # Normalize scores
        # --------------------------------

        category_scores = (
            self.normalize_scores(
                category_scores
            )
        )

        difficulty_scores = (
            self.normalize_scores(
                difficulty_scores
            )
        )

        language_scores = (
            self.normalize_scores(
                language_scores
            )
        )
        # --------------------------------
        # Update profile
        # --------------------------------

        profile.category_scores = (
            category_scores
        )

        profile.difficulty_scores = (
            difficulty_scores
        )

        profile.language_scores = (
            language_scores
        )

        profile.search_frequency = (
            search_count
        )

        profile.average_time_spent = (
            average_time
        )

        profile.average_scroll_depth = (
            average_scroll
        )
        profile.purchase_intent = (
            purchase_intent
        )
        profile.total_events = (
            total_events
        )

        # --------------------------------
        # Save
        # --------------------------------

        return self.profile_repository.update(
            db,
            profile,
        )
    def calculate_purchase_intent(
        self,
        events,
    ):
            """
            Calculates a normalized purchase-intent
            score from 0 to 1.
            """
    
            intent_score = 0.0
    
            for event in events:
    
                weight = self.calculate_recency_weight(
                    event
                )
    
                # -----------------------------
                # Product view
                # -----------------------------
    
                if event.event_type == "PRODUCT_VIEW":
    
                    intent_score += (
                        0.05 * weight
                    )
    
                # -----------------------------
                # Search
                # -----------------------------
    
                elif event.event_type == "SEARCH":
    
                    intent_score += (
                        0.03 * weight
                    )
    
                # -----------------------------
                # Filter
                # -----------------------------
    
                elif event.event_type == "FILTER":
    
                    intent_score += (
                        0.04 * weight
                    )
    
                # -----------------------------
                # Time spent
                # -----------------------------
    
                elif event.event_type == "TIME_SPENT":
    
                    if event.event_metadata:
    
                        metadata = event.event_metadata
    
                        if isinstance(
                            metadata,
                            str,
                        ):
                            import json
    
                            try:
                                metadata = json.loads(
                                    metadata
                                )
                            except json.JSONDecodeError:
                                metadata = {}
    
                        seconds = metadata.get(
                            "seconds",
                            0,
                        )
    
                        if seconds >= 60:
    
                            intent_score += (
                                0.10 * weight
                            )
    
                # -----------------------------
                # Scroll depth
                # -----------------------------
    
                elif event.event_type == "SCROLL_DEPTH":
    
                    if event.event_metadata:
    
                        metadata = event.event_metadata
    
                        if isinstance(
                            metadata,
                            str,
                        ):
                            import json
    
                            try:
                                metadata = json.loads(
                                    metadata
                                )
                            except json.JSONDecodeError:
                                metadata = {}
    
                        depth = metadata.get(
                            "depth",
                            0,
                        )
    
                        if depth >= 75:
    
                            intent_score += (
                                0.08 * weight
                            )
    
            # -----------------------------
            # Convert raw score to 0 → 1
            # -----------------------------

            purchase_intent = (
                1 - math.exp(-intent_score)
            )

            return round(
                purchase_intent,
                3,
            )
    
    def calculate_recency_weight(
    self,
    event,
):
        """
        Recent events receive higher weight.
        Weight decays exponentially with age.
        """

        now = datetime.now(UTC)

        event_time = event.created_at

        if event_time is None:
            return 1.0

        if event_time.tzinfo is None:
            event_time = event_time.replace(
                tzinfo=UTC
            )

        age_days = (
            now - event_time
        ).total_seconds() / 86400

        return math.exp(
            -0.10 * age_days
        )
    def normalize_scores(
    self,
    scores: dict,
):
        if not scores:
            return {}

        maximum = max(
            scores.values()
        )

        if maximum == 0:
            return scores

        return {
            key: round(
                value / maximum,
                3,
            )
            for key, value in scores.items()
        }
    

behavior_profile_service = (
    BehaviorProfileService()
)