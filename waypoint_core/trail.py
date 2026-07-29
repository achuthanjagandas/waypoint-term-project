from .distance import Distance


class Trail:
    """Represent one trail and protect its valid state."""

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
        """Create a Trail from an API-shaped dictionary."""
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

    def __eq__(self, other: object) -> bool:
        """Compare trails by identity rather than changing details."""
        if not isinstance(other, Trail):
            return NotImplemented

        return self.trail_id == other.trail_id