import unittest

from waypoint_core import (
    BackpackingRoute,
    DayHike,
    Distance,
    Trail,
    TrailRun,
)


class TrailTests(unittest.TestCase):

    def setUp(self):
        Trail.set_default_unit("km")

    def tearDown(self):
        Trail.set_default_unit("km")

    @staticmethod
    def create_day_hike(
        trail_id: int = 101,
        name: str = "Maple Ridge",
    ) -> DayHike:
        return DayHike(
            trail_id=trail_id,
            name=name,
            distance=Distance(6.5, "km"),
            elevation_gain_m=240,
            difficulty="moderate",
        )

    def test_trail_cannot_be_instantiated_directly(self):
        with self.assertRaises(TypeError):
            Trail(
                trail_id=101,
                name="Maple Ridge",
                distance=Distance(6.5, "km"),
                elevation_gain_m=240,
                difficulty="moderate",
            )

    def test_incomplete_subclass_cannot_be_instantiated(self):
        class IncompleteTrail(Trail):
            pass

        with self.assertRaises(TypeError):
            IncompleteTrail(
                trail_id=101,
                name="Incomplete Trail",
                distance=Distance(5, "km"),
                elevation_gain_m=100,
                difficulty="easy",
            )

    def test_day_hike_stores_its_information(self):
        distance = Distance(6.5, "km")

        trail = DayHike(
            trail_id=101,
            name="Maple Ridge",
            distance=distance,
            elevation_gain_m=240,
            difficulty="moderate",
        )

        self.assertEqual(trail.trail_id, 101)
        self.assertEqual(trail.name, "Maple Ridge")
        self.assertIs(trail.distance, distance)
        self.assertEqual(trail.elevation_gain_m, 240.0)
        self.assertEqual(trail.difficulty, "moderate")

    def test_distance_must_be_a_distance_object(self):
        with self.assertRaises(TypeError):
            DayHike(
                trail_id=101,
                name="Maple Ridge",
                distance=6.5,
                elevation_gain_m=240,
                difficulty="moderate",
            )

    def test_blank_name_is_rejected(self):
        with self.assertRaises(ValueError):
            DayHike(
                trail_id=101,
                name="   ",
                distance=Distance(6.5, "km"),
                elevation_gain_m=240,
                difficulty="moderate",
            )

    def test_negative_elevation_gain_is_rejected(self):
        with self.assertRaises(ValueError):
            DayHike(
                trail_id=101,
                name="Maple Ridge",
                distance=Distance(6.5, "km"),
                elevation_gain_m=-20,
                difficulty="moderate",
            )

    def test_invalid_difficulty_is_rejected(self):
        with self.assertRaises(ValueError):
            DayHike(
                trail_id=101,
                name="Maple Ridge",
                distance=Distance(6.5, "km"),
                elevation_gain_m=240,
                difficulty="extreme",
            )

    def test_set_difficulty_changes_valid_difficulty(self):
        trail = self.create_day_hike()

        trail.set_difficulty("hard")

        self.assertEqual(trail.difficulty, "hard")

    def test_invalid_difficulty_change_is_rejected(self):
        trail = self.create_day_hike()

        with self.assertRaises(ValueError):
            trail.set_difficulty("impossible")

        self.assertEqual(trail.difficulty, "moderate")

    def test_from_dict_populates_day_hike(self):
        data = {
            "id": 201,
            "name": "Lake View",
            "distance": 8.4,
            "unit": "km",
            "elevation_gain_m": 310,
            "difficulty": "hard",
        }

        trail = DayHike.from_dict(data)

        self.assertEqual(trail.trail_id, 201)
        self.assertEqual(trail.name, "Lake View")
        self.assertEqual(trail.distance.magnitude, 8.4)
        self.assertEqual(trail.distance.unit, "km")
        self.assertEqual(trail.elevation_gain_m, 310.0)
        self.assertEqual(trail.difficulty, "hard")

    def test_from_dict_uses_default_unit(self):
        data = {
            "id": 201,
            "name": "Lake View",
            "distance": 8.4,
            "elevation_gain_m": 310,
            "difficulty": "hard",
        }

        trail = DayHike.from_dict(data)

        self.assertEqual(trail.distance.unit, "km")

    def test_default_unit_change_affects_only_new_trails(self):
        first_trail = DayHike.from_dict(
            {
                "id": 201,
                "name": "Lake View",
                "distance": 8.4,
                "elevation_gain_m": 310,
                "difficulty": "hard",
            }
        )

        Trail.set_default_unit("mi")

        second_trail = DayHike.from_dict(
            {
                "id": 202,
                "name": "Forest Path",
                "distance": 5.2,
                "elevation_gain_m": 120,
                "difficulty": "easy",
            }
        )

        self.assertEqual(first_trail.distance.unit, "km")
        self.assertEqual(second_trail.distance.unit, "mi")

    def test_trails_with_same_id_compare_equal(self):
        first_trail = self.create_day_hike(
            trail_id=101,
            name="Maple Ridge",
        )
        second_trail = self.create_day_hike(
            trail_id=101,
            name="Updated Maple Ridge",
        )

        self.assertEqual(first_trail, second_trail)

    def test_trails_with_different_ids_are_not_equal(self):
        first_trail = self.create_day_hike(trail_id=101)
        second_trail = self.create_day_hike(trail_id=102)

        self.assertNotEqual(first_trail, second_trail)

    def test_day_hike_estimated_time(self):
        trail = DayHike(
            trail_id=1,
            name="Day Trail",
            distance=Distance(8, "km"),
            elevation_gain_m=600,
            difficulty="moderate",
            pace_kmh=4,
        )

        self.assertAlmostEqual(trail.estimated_time(), 3.0)

    def test_backpacking_route_estimated_time(self):
        trail = BackpackingRoute(
            trail_id=2,
            name="Backpacking Trail",
            distance=Distance(9, "km"),
            elevation_gain_m=500,
            difficulty="hard",
            days=3,
            pace_kmh=3,
        )

        self.assertAlmostEqual(trail.estimated_time(), 5.0)

    def test_trail_run_estimated_time(self):
        trail = TrailRun(
            trail_id=3,
            name="Running Trail",
            distance=Distance(9, "km"),
            elevation_gain_m=900,
            difficulty="hard",
            pace_kmh=9,
        )

        self.assertAlmostEqual(trail.estimated_time(), 2.0)

    def test_subclass_packing_list_extends_parent_list(self):
        trail = BackpackingRoute(
            trail_id=2,
            name="Backpacking Trail",
            distance=Distance(9, "km"),
            elevation_gain_m=500,
            difficulty="hard",
        )

        items = trail.packing_list()

        self.assertIn("water", items)
        self.assertIn("first aid kit", items)
        self.assertIn("tent", items)
        self.assertIn("sleeping bag", items)


if __name__ == "__main__":
    unittest.main()