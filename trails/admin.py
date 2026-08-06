from django.contrib import admin

from .models import Park, Trail


@admin.register(Park)
class ParkAdmin(admin.ModelAdmin):
    """Configure Park records in the Django administration site."""

    list_display = (
        "name",
        "region",
    )
    search_fields = (
        "name",
        "region",
    )
    ordering = (
        "name",
    )


@admin.register(Trail)
class TrailAdmin(admin.ModelAdmin):
    """Configure Trail records in the Django administration site."""

    list_display = (
        "name",
        "park",
        "distance_km",
        "elevation_gain",
        "difficulty",
        "is_open",
        "added",
    )
    search_fields = (
        "name",
        "park__name",
        "park__region",
    )
    list_filter = (
        "park",
        "difficulty",
        "is_open",
    )
    ordering = (
        "name",
    )