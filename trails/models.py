from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Trail(models.Model):
    """Store a trail that can be displayed in the Waypoint catalog."""

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MODERATE = "moderate", "Moderate"
        EXPERT = "expert", "Expert"

    name = models.CharField(
        max_length=150,
    )
    distance_km = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    elevation_gain = models.IntegerField(
        validators=[MinValueValidator(0)],
    )
    difficulty = models.CharField(
        max_length=10,
        choices=Difficulty.choices,
        default=Difficulty.EASY,
    )
    is_open = models.BooleanField(
        default=True,
    )
    added = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        """Return the trail name in the admin and Django shell."""
        return self.name