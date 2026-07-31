from waypoint_core import DayHike, Distance, Itinerary, Trail


def main():
    """Demonstrate the mandatory Week 7 Waypoint behaviours."""

    print("WAYPOINT — WEEK 7 DEMONSTRATION")
    print("-" * 40)

    lake_trail = DayHike.from_dict(
        {
            "id": 101,
            "name": "Lake Trail",
            "distance": 2.5,
            "unit": "km",
            "elevation_gain_m": 100,
            "difficulty": "easy",
        }
    )

    forest_trail = DayHike(
        trail_id=102,
        name="Forest Trail",
        distance=Distance(3.5, "km"),
        elevation_gain_m=150,
        difficulty="moderate",
    )

    hill_trail = DayHike(
        trail_id=103,
        name="Hill Trail",
        distance=Distance(4, "km"),
        elevation_gain_m=220,
        difficulty="hard",
    )

    itinerary = Itinerary(
        [lake_trail, forest_trail, hill_trail]
    )

    total_km = itinerary.total_distance("km")
    total_mi = itinerary.total_distance("mi")

    print(f"Number of trails: {len(itinerary.trails)}")
    print(
        f"Total distance: "
        f"{total_km.magnitude:.2f} {total_km.unit}"
    )
    print(
        f"Total in miles: "
        f"{total_mi.magnitude:.2f} {total_mi.unit}"
    )

    updated_lake_record = DayHike(
        trail_id=101,
        name="Updated Lake Trail",
        distance=Distance(3, "km"),
        elevation_gain_m=120,
        difficulty="moderate",
    )

    print(
        "Matching trail IDs compare equal:",
        lake_trail == updated_lake_record,
    )

    first_itinerary = Itinerary()
    second_itinerary = Itinerary()

    first_itinerary.add_trail(lake_trail)

    print(
        "Independent itinerary lengths:",
        len(first_itinerary.trails),
        "and",
        len(second_itinerary.trails),
    )

    original_default = Trail.default_unit

    existing_trail = DayHike.from_dict(
        {
            "id": 201,
            "name": "Existing Trail",
            "distance": 5,
            "elevation_gain_m": 100,
            "difficulty": "easy",
        }
    )

    Trail.set_default_unit("mi")

    future_trail = DayHike.from_dict(
        {
            "id": 202,
            "name": "Future Trail",
            "distance": 5,
            "elevation_gain_m": 100,
            "difficulty": "easy",
        }
    )

    print(
        "Existing trail unit:",
        existing_trail.distance.unit,
    )
    print(
        "New trail unit after default change:",
        future_trail.distance.unit,
    )

    Trail.set_default_unit(original_default)


if __name__ == "__main__":
    main()