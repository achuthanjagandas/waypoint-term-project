from django.shortcuts import render

from .forms import TrailReportForm


SAMPLE_TRAILS = [
    {
        "name": "Lake View Trail",
        "distance": "5.2 km",
        "difficulty": "Easy",
    },
    {
        "name": "Forest Ridge",
        "distance": "8.4 km",
        "difficulty": "Moderate",
    },
    {
        "name": "Summit Loop",
        "distance": "12.1 km",
        "difficulty": "Hard",
    },
    {
        "name": "River Path",
        "distance": "3.8 km",
        "difficulty": "Easy",
    },
]


CATALOG_TRAILS = [
    {
        "name": "Lake View Trail",
        "distance_km": 5.25,
        "elevation_gain": 120,
        "difficulty": "easy",
        "is_open": True,
    },
    {
        "name": "Forest Ridge",
        "distance_km": 8.44,
        "elevation_gain": 340,
        "difficulty": "moderate",
        "is_open": True,
    },
    {
        "name": "Summit Loop",
        "distance_km": 12.08,
        "elevation_gain": 780,
        "difficulty": "expert",
        "is_open": True,
    },
    {
        "name": "River Path",
        "distance_km": 3.76,
        "elevation_gain": 45,
        "difficulty": "easy",
        "is_open": False,
    },
    {
        "name": "Pine Valley Route",
        "distance_km": 9.63,
        "elevation_gain": 410,
        "difficulty": "moderate",
        "is_open": True,
    },
    {
        "name": "Granite Peak Trail",
        "distance_km": 14.91,
        "elevation_gain": 960,
        "difficulty": "expert",
        "is_open": False,
    },
]


def home(request):
    """Display the Waypoint homepage."""
    context = {
        "greeting": "Welcome to Waypoint",
        "message": "Find trails and plan your next outdoor adventure.",
    }

    return render(request, "home.html", context)


def report_trail(request):
    """Display and process the trail-report form."""
    if request.method == "POST":
        form = TrailReportForm(request.POST)

        if form.is_valid():
            context = {
                "reporter_name": form.cleaned_data["reporter_name"],
                "trail_name": form.cleaned_data["trail_name"],
            }

            return render(request, "report_thanks.html", context)
    else:
        form = TrailReportForm()

    return render(
        request,
        "report_form.html",
        {"form": form},
    )


def search_trails(request):
    """Search the temporary trail catalogue by name."""
    query = request.GET.get("q", "").strip()

    if query:
        results = [
            trail
            for trail in SAMPLE_TRAILS
            if query.casefold() in trail["name"].casefold()
        ]
    else:
        results = []

    context = {
        "query": query,
        "results": results,
        "search_performed": bool(query),
    }

    return render(request, "search.html", context)


def catalog(request):
    """Display the temporary Week 11 trail catalogue."""
    context = {
        "trails": CATALOG_TRAILS,
    }

    return render(request, "catalog.html", context)