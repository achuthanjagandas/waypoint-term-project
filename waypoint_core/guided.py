from collections.abc import Iterable

from .distance import Distance
from .mixins import ElevationMixin, RatingMixin
from .trail import DayHike


class GuidedDayHike(ElevationMixin, RatingMixin, DayHike):
    """A day hike led by a guide for a limited group."""

    def __init__(
        self,
        trail_id: int,
        name: str,
        distance: Distance,
        elevation_gain_m: float,
        difficulty: str,
        guide_name: str,
        group_size: int = 8,
        pace_kmh: float = 4.0,
        ratings: Iterable[float] | None = None,
    ):
        super().__init__(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
            pace_kmh=pace_kmh,
        )

        self._guide_name = self._validate_guide_name(guide_name)
        self._group_size = self._validate_group_size(group_size)
        self._ratings: list[float] = []

        if ratings is not None:
            for rating in ratings:
                self.add_rating(rating)

    @property
    def guide_name(self) -> str:
        """Return the guide's name."""
        return self._guide_name

    @property
    def group_size(self) -> int:
        """Return the maximum group size."""
        return self._group_size

    @staticmethod
    def _validate_guide_name(guide_name: str) -> str:
        """Validate and clean the guide's name."""
        if not isinstance(guide_name, str):
            raise TypeError("Guide name must be a string.")

        cleaned_name = guide_name.strip()

        if not cleaned_name:
            raise ValueError("Guide name cannot be empty.")

        return cleaned_name

    @staticmethod
    def _validate_group_size(group_size: int) -> int:
        """Validate a positive group size."""
        if isinstance(group_size, bool) or not isinstance(
            group_size,
            int,
        ):
            raise TypeError("Group size must be an integer.")

        if group_size < 1:
            raise ValueError("Group size must be at least one.")

        return group_size

    def estimated_time(self) -> float:
        """
        Extend the normal day-hike estimate.

        A guided hike includes an additional 30-minute safety briefing.
        """
        return super().estimated_time() + 0.5

    def summary(self) -> str:
        """Extend the day-hike summary with guided-trip details."""
        return (
            f"{super().summary()} "
            f"Guide: {self.guide_name}; "
            f"maximum group size: {self.group_size}."
        )

    def packing_list(self) -> list[str]:
        """Extend the day-hike list with guided-trip documentation."""
        items = super().packing_list()
        items.append("booking confirmation")
        return items