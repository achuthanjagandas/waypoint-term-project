from django.shortcuts import render

from .models import Park, Trail


def catalog(request):
    """Display open trails, optionally filtered by park."""
    parks = Park.objects.order_by("name")

    trails = (
        Trail.objects.filter(is_open=True)
        .select_related("park")
        .order_by("distance_km")
    )

    selected_park = None
    selected_park_id = request.GET.get("park", "").strip()

    if selected_park_id.isdigit():
        selected_park = parks.filter(pk=int(selected_park_id)).first()

        if selected_park is not None:
            trails = trails.filter(park=selected_park)

    context = {
        "parks": parks,
        "selected_park": selected_park,
        "trails": trails,
    }

    return render(request, "catalog.html", context)