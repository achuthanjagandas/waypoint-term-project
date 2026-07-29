class Distance:
    """Represent a non-negative distance in kilometres or miles."""

    VALID_UNITS = ("km", "mi")
    KM_TO_MILES = 0.621371

    def __init__(self, magnitude: float, unit: str):
        self._magnitude = self._validate_magnitude(magnitude)
        self._unit = self._validate_unit(unit)

    @property
    def magnitude(self) -> float:
        """Return the distance magnitude without allowing direct changes."""
        return self._magnitude

    @property
    def unit(self) -> str:
        """Return the distance unit without allowing direct changes."""
        return self._unit

    @staticmethod
    def _validate_magnitude(magnitude: float) -> float:
        """Validate and return the magnitude as a float."""
        if isinstance(magnitude, bool) or not isinstance(magnitude, (int, float)):
            raise TypeError("Magnitude must be a number.")

        if magnitude < 0:
            raise ValueError("Distance cannot be negative.")

        return float(magnitude)

    @classmethod
    def _validate_unit(cls, unit: str) -> str:
        """Validate and normalize the distance unit."""
        if not isinstance(unit, str):
            raise TypeError("Unit must be a string.")

        normalized_unit = unit.strip().lower()

        if normalized_unit not in cls.VALID_UNITS:
            raise ValueError("Unit must be 'km' or 'mi'.")

        return normalized_unit

    def convert(self, target_unit: str) -> "Distance":
        """Return a new Distance converted to the requested unit."""
        target_unit = self._validate_unit(target_unit)

        if target_unit == self.unit:
            return Distance(self.magnitude, self.unit)

        if self.unit == "km":
            converted_magnitude = self.magnitude * self.KM_TO_MILES
        else:
            converted_magnitude = self.magnitude / self.KM_TO_MILES

        return Distance(converted_magnitude, target_unit)