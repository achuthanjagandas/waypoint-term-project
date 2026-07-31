from math import isclose


class Distance:
    """
    Represent a non-negative distance in kilometres or miles.

    Mixed-unit policy:
    When two Distance objects use different units, the right-hand
    distance is automatically converted into the left-hand distance's
    unit before arithmetic or comparison.
    """

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
        if isinstance(magnitude, bool) or not isinstance(
            magnitude,
            (int, float),
        ):
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

    def _converted_other(self, other: object) -> "Distance":
        """Validate another operand and convert it to this object's unit."""
        if not isinstance(other, Distance):
            return NotImplemented

        return other.convert(self.unit)

    def __add__(self, other: object) -> "Distance":
        """Add two distances and return the result in the left unit."""
        converted_other = self._converted_other(other)

        if converted_other is NotImplemented:
            return NotImplemented

        return Distance(
            self.magnitude + converted_other.magnitude,
            self.unit,
        )

    def __sub__(self, other: object) -> "Distance":
        """
        Subtract one distance from another.

        The result uses the left-hand unit. A subtraction that would
        create a negative distance raises ValueError.
        """
        converted_other = self._converted_other(other)

        if converted_other is NotImplemented:
            return NotImplemented

        result = self.magnitude - converted_other.magnitude

        if result < 0 and not isclose(
            result,
            0.0,
            rel_tol=1e-9,
            abs_tol=1e-9,
        ):
            raise ValueError(
                "Distance subtraction cannot produce a negative result."
            )

        if isclose(
            result,
            0.0,
            rel_tol=1e-9,
            abs_tol=1e-9,
        ):
            result = 0.0

        return Distance(result, self.unit)

    def __eq__(self, other: object) -> bool:
        """Compare two distances after converting to the left unit."""
        converted_other = self._converted_other(other)

        if converted_other is NotImplemented:
            return NotImplemented

        return isclose(
            self.magnitude,
            converted_other.magnitude,
            rel_tol=1e-9,
            abs_tol=1e-9,
        )

    def __lt__(self, other: object) -> bool:
        """Return whether this distance is shorter than another."""
        converted_other = self._converted_other(other)

        if converted_other is NotImplemented:
            return NotImplemented

        return self.magnitude < converted_other.magnitude

    def __gt__(self, other: object) -> bool:
        """Return whether this distance is longer than another."""
        converted_other = self._converted_other(other)

        if converted_other is NotImplemented:
            return NotImplemented

        return self.magnitude > converted_other.magnitude

    def __str__(self) -> str:
        """Return a readable distance for users."""
        return f"{self.magnitude:.2f} {self.unit}"

    def __repr__(self) -> str:
        """Return a developer-focused representation."""
        return (
            f"Distance(magnitude={self.magnitude!r}, "
            f"unit={self.unit!r})"
        )