from django.shortcuts import render

from .models import Trail


def catalog(request):
    """Display open trails ordered from shortest to longest."""
    trails = Trail.objects.filter(is_open=True).order_by("distance_km")

    context = {
        "trails": trails,
    }

    return render(request, "catalog.html", context)