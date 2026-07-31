class ElevationMixin:
    """Provide calculations related to trail elevation."""

    def grade_percent(self) -> float:
        """Return elevation gain as a percentage of trail distance."""
        distance_m = self.distance.convert("km").magnitude * 1000

        if distance_m == 0:
            return 0.0

        return (self.elevation_gain_m / distance_m) * 100

    def feature_label(self) -> str:
        """Return a label used to demonstrate method resolution order."""
        return "elevation-aware"


class RatingMixin:
    """Provide trail-rating behaviour."""

    @property
    def ratings(self) -> tuple[float, ...]:
        """Return ratings without exposing the internal list."""
        return tuple(self._ratings)

    @property
    def average_rating(self) -> float:
        """Return the average rating or zero when none exist."""
        if not self._ratings:
            return 0.0

        return sum(self._ratings) / len(self._ratings)

    def add_rating(self, rating: float) -> None:
        """Add a rating between zero and five."""
        if isinstance(rating, bool) or not isinstance(
            rating,
            (int, float),
        ):
            raise TypeError("Rating must be a number.")

        if not 0 <= rating <= 5:
            raise ValueError("Rating must be between 0 and 5.")

        self._ratings.append(float(rating))

    def feature_label(self) -> str:
        """Return a label used to demonstrate method resolution order."""
        return "community-rated"