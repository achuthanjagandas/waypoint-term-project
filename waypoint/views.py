from django.shortcuts import render


def home(request):
    """Display the Waypoint homepage."""
    context = {
        "greeting": "Welcome to Waypoint",
        "message": "Find trails and plan your next outdoor adventure.",
    }

    return render(request, "home.html", context)