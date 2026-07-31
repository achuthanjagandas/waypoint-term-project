from waypoint_core import (
    BackpackingRoute,
    DayHike,
    Distance,
    FakeTrail,
    GuidedDayHike,
    TrailRun,
    print_estimated_times,
)


def main():
    """Demonstrate the mandatory Week 8 behaviours."""

    day_hike = DayHike(
        trail_id=1,
        name="Lake Day Hike",
        distance=Distance(8, "km"),
        elevation_gain_m=600,
        difficulty="moderate",
    )

    backpacking_route = BackpackingRoute(
        trail_id=2,
        name="Forest Backpacking Route",
        distance=Distance(12, "km"),
        elevation_gain_m=500,
        difficulty="hard",
        days=2,
    )

    trail_run = TrailRun(
        trail_id=3,
        name="Ridge Trail Run",
        distance=Distance(10, "km"),
        elevation_gain_m=450,
        difficulty="hard",
    )

    guided_hike = GuidedDayHike(
        trail_id=4,
        name="Guided Lookout Hike",
        distance=Distance(6, "km"),
        elevation_gain_m=300,
        difficulty="moderate",
        guide_name="Maya",
        group_size=8,
        ratings=[4, 5, 4],
    )

    fake_trail = FakeTrail(
        name="Duck-Typed Test Trail",
        hours=1.25,
    )

    print("WAYPOINT — WEEK 8 DEMONSTRATION")
    print("-" * 42)
    print("Polymorphic estimated-time loop:")

    print_estimated_times(
        [
            day_hike,
            backpacking_route,
            trail_run,
            guided_hike,
            fake_trail,
        ]
    )

    print()
    print("Guided hike summary:")
    print(guided_hike.summary())

    print()
    print(
        "Guided hike grade:",
        f"{guided_hike.grade_percent():.2f}%",
    )
    print(
        "Guided hike average rating:",
        f"{guided_hike.average_rating:.2f}",
    )
    print(
        "Shared method selected by MRO:",
        guided_hike.feature_label(),
    )

    mro_names = " -> ".join(
        class_type.__name__
        for class_type in GuidedDayHike.__mro__
    )

    print("GuidedDayHike MRO:")
    print(mro_names)

    print()
    print("Distance operator overloading:")

    combined = Distance(5, "km") + Distance(1, "mi")
    remaining = Distance(10, "km") - Distance(2, "mi")

    print("5 km + 1 mi =", combined)
    print("10 km - 2 mi =", remaining)
    print(
        "1 mi equals its kilometre conversion:",
        Distance(1, "mi")
        == Distance(1, "mi").convert("km"),
    )

    sorted_distances = sorted(
        [
            Distance(5, "km"),
            Distance(1, "mi"),
            Distance(3, "km"),
        ]
    )

    print(
        "Sorted distances:",
        ", ".join(
            str(distance)
            for distance in sorted_distances
        ),
    )

    print(
        "Developer representation:",
        repr(Distance(5, "km")),
    )


if __name__ == "__main__":
    main()