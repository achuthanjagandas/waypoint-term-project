from collections.abc import Iterable

from .distance import Distance
from .trail import Trail


class Itinerary:
    """Represent an ordered collection of trails for one trip."""

    def __init__(self, trails: Iterable[Trail] | None = None):
        self._trails: list[Trail] = []

        if trails is not None:
            for trail in trails:
                self.add_trail(trail)

    @property
    def trails(self) -> tuple[Trail, ...]:
        """Return the trails in order without exposing the internal list."""
        return tuple(self._trails)

    def add_trail(self, trail: Trail) -> None:
        """Add one valid Trail to the end of the itinerary."""
        if not isinstance(trail, Trail):
            raise TypeError("Only Trail objects can be added.")

        self._trails.append(trail)

    def total_distance(self, unit: str = "km") -> Distance:
        """Return the combined trail distance in the requested unit."""
        total_magnitude = 0.0

        for trail in self._trails:
            converted_distance = trail.distance.convert(unit)
            total_magnitude += converted_distance.magnitude

        return Distance(total_magnitude, unit)