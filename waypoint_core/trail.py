from abc import ABC, abstractmethod

from .distance import Distance


class Trail(ABC):
    """Abstract base class containing behaviour shared by all trails."""

    ALLOWED_DIFFICULTIES = ("easy", "moderate", "hard", "expert")
    default_unit = "km"

    def __init__(
        self,
        trail_id: int,
        name: str,
        distance: Distance,
        elevation_gain_m: float,
        difficulty: str,
    ):
        if not isinstance(distance, Distance):
            raise TypeError("Distance must be a Distance object.")

        self._trail_id = trail_id
        self._name = self._validate_name(name)
        self._distance = distance
        self._elevation_gain_m = self._validate_elevation_gain(
            elevation_gain_m
        )
        self.__difficulty = self._validate_difficulty(difficulty)

    @property
    def trail_id(self) -> int:
        """Return the trail identity."""
        return self._trail_id

    @property
    def name(self) -> str:
        """Return the trail name."""
        return self._name

    @property
    def distance(self) -> Distance:
        """Return the trail's Distance object."""
        return self._distance

    @property
    def elevation_gain_m(self) -> float:
        """Return the elevation gain in metres."""
        return self._elevation_gain_m

    @property
    def difficulty(self) -> str:
        """Return the validated difficulty."""
        return self.__difficulty

    def set_difficulty(self, difficulty: str) -> None:
        """Change the difficulty after validating the new value."""
        self.__difficulty = self._validate_difficulty(difficulty)

    def distance_in_km(self) -> float:
        """Return the trail distance converted to kilometres."""
        return self.distance.convert("km").magnitude

    def packing_list(self) -> list[str]:
        """Return equipment required for every trail type."""
        return [
            "water",
            "first aid kit",
            "map",
        ]

    @abstractmethod
    def estimated_time(self) -> float:
        """Return the estimated completion time in hours."""
        raise NotImplementedError

    @abstractmethod
    def summary(self) -> str:
        """Return a short human-readable trail description."""
        raise NotImplementedError

    @classmethod
    def set_default_unit(cls, unit: str) -> None:
        """Set the unit used by future dictionary-created trails."""
        if not isinstance(unit, str):
            raise TypeError("Default unit must be a string.")

        normalized_unit = unit.strip().lower()

        if normalized_unit not in Distance.VALID_UNITS:
            raise ValueError("Default unit must be 'km' or 'mi'.")

        cls.default_unit = normalized_unit

    @classmethod
    def from_dict(cls, data: dict) -> "Trail":
        """Create a concrete trail type from an API-shaped dictionary."""
        if not isinstance(data, dict):
            raise TypeError("Trail data must be a dictionary.")

        unit = data.get("unit", cls.default_unit)
        distance = Distance(data["distance"], unit)

        return cls(
            trail_id=data["id"],
            name=data["name"],
            distance=distance,
            elevation_gain_m=data["elevation_gain_m"],
            difficulty=data["difficulty"],
        )

    @staticmethod
    def _validate_name(name: str) -> str:
        """Validate and clean the trail name."""
        if not isinstance(name, str):
            raise TypeError("Trail name must be a string.")

        cleaned_name = name.strip()

        if not cleaned_name:
            raise ValueError("Trail name cannot be empty.")

        return cleaned_name

    @staticmethod
    def _validate_elevation_gain(elevation_gain_m: float) -> float:
        """Validate and return a non-negative elevation gain."""
        if (
            isinstance(elevation_gain_m, bool)
            or not isinstance(elevation_gain_m, (int, float))
        ):
            raise TypeError("Elevation gain must be a number.")

        if elevation_gain_m < 0:
            raise ValueError("Elevation gain cannot be negative.")

        return float(elevation_gain_m)

    @staticmethod
    def _validate_difficulty(difficulty: str) -> str:
        """Validate and normalize a difficulty value."""
        if not isinstance(difficulty, str):
            raise TypeError("Difficulty must be a string.")

        normalized_difficulty = difficulty.strip().lower()

        if normalized_difficulty not in Trail.ALLOWED_DIFFICULTIES:
            allowed = ", ".join(Trail.ALLOWED_DIFFICULTIES)
            raise ValueError(
                f"Difficulty must be one of: {allowed}."
            )

        return normalized_difficulty

    @staticmethod
    def _validate_positive_number(
        value: float,
        field_name: str,
    ) -> float:
        """Validate a positive numeric value."""
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{field_name} must be a number.")

        if value <= 0:
            raise ValueError(f"{field_name} must be greater than zero.")

        return float(value)

    def __eq__(self, other: object) -> bool:
        """Compare trails by identity rather than changing details."""
        if not isinstance(other, Trail):
            return NotImplemented

        return self.trail_id == other.trail_id


class DayHike(Trail):
    """A trail normally completed within one day."""

    def __init__(
        self,
        trail_id: int,
        name: str,
        distance: Distance,
        elevation_gain_m: float,
        difficulty: str,
        pace_kmh: float = 4.0,
    ):
        super().__init__(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
        )
        self._pace_kmh = self._validate_positive_number(
            pace_kmh,
            "Pace",
        )

    @property
    def pace_kmh(self) -> float:
        """Return the planned hiking pace."""
        return self._pace_kmh

    def estimated_time(self) -> float:
        """
        Estimate hours using distance plus elevation.

        Formula:
        distance in km / pace + elevation gain / 600
        """
        distance_hours = self.distance_in_km() / self.pace_kmh
        elevation_hours = self.elevation_gain_m / 600

        return distance_hours + elevation_hours

    def summary(self) -> str:
        """Return a summary of the day hike."""
        return (
            f"{self.name} is a {self.difficulty} day hike "
            f"covering {self.distance.magnitude:.1f} "
            f"{self.distance.unit}."
        )

    def packing_list(self) -> list[str]:
        """Extend the general list with day-hike equipment."""
        items = super().packing_list()
        items.extend(
            [
                "snacks",
                "sun protection",
            ]
        )
        return items


class BackpackingRoute(Trail):
    """A multi-day trail completed while carrying overnight gear."""

    def __init__(
        self,
        trail_id: int,
        name: str,
        distance: Distance,
        elevation_gain_m: float,
        difficulty: str,
        days: int = 2,
        pace_kmh: float = 3.0,
    ):
        super().__init__(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
        )

        if isinstance(days, bool) or not isinstance(days, int):
            raise TypeError("Days must be an integer.")

        if days < 1:
            raise ValueError("Days must be at least one.")

        self._days = days
        self._pace_kmh = self._validate_positive_number(
            pace_kmh,
            "Pace",
        )

    @property
    def days(self) -> int:
        """Return the planned number of days."""
        return self._days

    @property
    def pace_kmh(self) -> float:
        """Return the planned backpacking pace."""
        return self._pace_kmh

    def estimated_time(self) -> float:
        """
        Estimate active hours including overnight setup.

        Formula:
        distance in km / pace
        + elevation gain / 500
        + 0.5 hour for each overnight stop
        """
        distance_hours = self.distance_in_km() / self.pace_kmh
        elevation_hours = self.elevation_gain_m / 500
        setup_hours = (self.days - 1) * 0.5

        return distance_hours + elevation_hours + setup_hours

    def summary(self) -> str:
        """Return a summary of the backpacking route."""
        return (
            f"{self.name} is a {self.days}-day "
            f"{self.difficulty} backpacking route."
        )

    def packing_list(self) -> list[str]:
        """Extend the general list with overnight equipment."""
        items = super().packing_list()
        items.extend(
            [
                "tent",
                "sleeping bag",
                "cooking kit",
            ]
        )
        return items


class TrailRun(Trail):
    """A trail intended to be completed by running."""

    def __init__(
        self,
        trail_id: int,
        name: str,
        distance: Distance,
        elevation_gain_m: float,
        difficulty: str,
        pace_kmh: float = 8.0,
    ):
        super().__init__(
            trail_id=trail_id,
            name=name,
            distance=distance,
            elevation_gain_m=elevation_gain_m,
            difficulty=difficulty,
        )
        self._pace_kmh = self._validate_positive_number(
            pace_kmh,
            "Pace",
        )

    @property
    def pace_kmh(self) -> float:
        """Return the planned running pace."""
        return self._pace_kmh

    def estimated_time(self) -> float:
        """
        Estimate running hours including elevation.

        Formula:
        distance in km / pace + elevation gain / 900
        """
        distance_hours = self.distance_in_km() / self.pace_kmh
        elevation_hours = self.elevation_gain_m / 900

        return distance_hours + elevation_hours

    def summary(self) -> str:
        """Return a summary of the trail run."""
        return (
            f"{self.name} is a {self.difficulty} trail run "
            f"covering {self.distance.magnitude:.1f} "
            f"{self.distance.unit}."
        )

    def packing_list(self) -> list[str]:
        """Extend the general list with running equipment."""
        items = super().packing_list()
        items.extend(
            [
                "running vest",
                "energy gel",
            ]
        )
        return items