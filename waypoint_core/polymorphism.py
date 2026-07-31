from collections.abc import Iterable


class FakeTrail:
    """
    A duck-typed trail used without inheriting from Trail.

    It works in the polymorphic loop because it provides the attributes
    and method that the loop needs.
    """

    def __init__(self, name: str, hours: float):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Fake trail name cannot be empty.")

        if isinstance(hours, bool) or not isinstance(
            hours,
            (int, float),
        ):
            raise TypeError("Hours must be a number.")

        if hours < 0:
            raise ValueError("Hours cannot be negative.")

        self.name = name.strip()
        self._hours = float(hours)

    def estimated_time(self) -> float:
        """Return the predetermined test time."""
        return self._hours


def print_estimated_times(trails: Iterable[object]) -> None:
    """Print estimated time for any object supporting the required API."""
    for trail in trails:
        print(
            f"{trail.name}: "
            f"{trail.estimated_time():.2f} hours"
        )