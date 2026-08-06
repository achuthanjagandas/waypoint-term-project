from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models


class Park(models.Model):
    """Store a park that contains one or more trails."""

    name = models.CharField(
        max_length=150,
    )
    region = models.CharField(
        max_length=150,
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        """Return a readable park name and region."""
        return f"{self.name} ({self.region})"


class Trail(models.Model):
    """Store a trail that can be displayed in the Waypoint catalog."""

    class Difficulty(models.TextChoices):
        EASY = "easy", "Easy"
        MODERATE = "moderate", "Moderate"
        EXPERT = "expert", "Expert"

    name = models.CharField(
        max_length=150,
    )
    park = models.ForeignKey(
        Park,
        on_delete=models.PROTECT,
        related_name="trails",
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