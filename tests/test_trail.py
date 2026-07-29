import unittest

from waypoint_core import Distance, Trail


class TrailTests(unittest.TestCase):

    def setUp(self):
        Trail.set_default_unit("km")

    def tearDown(self):
        Trail.set_default_unit("km")

    def test_trail_stores_its_information(self):
        distance = Distance(6.5, "km")

        trail = Trail(
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
            Trail(
                trail_id=101,
                name="Maple Ridge",
                distance=6.5,
                elevation_gain_m=240,
                difficulty="moderate",
            )

    def test_blank_name_is_rejected(self):
        with self.assertRaises(ValueError):
            Trail(
                trail_id=101,
                name="   ",
                distance=Distance(6.5, "km"),
                elevation_gain_m=240,
                difficulty="moderate",
            )

    def test_negative_elevation_gain_is_rejected(self):
        with self.assertRaises(ValueError):
            Trail(
                trail_id=101,
                name="Maple Ridge",
                distance=Distance(6.5, "km"),
                elevation_gain_m=-20,
                difficulty="moderate",
            )

    def test_invalid_difficulty_is_rejected(self):
        with self.assertRaises(ValueError):
            Trail(
                trail_id=101,
                name="Maple Ridge",
                distance=Distance(6.5, "km"),
                elevation_gain_m=240,
                difficulty="extreme",
            )

    def test_set_difficulty_changes_valid_difficulty(self):
        trail = Trail(
            trail_id=101,
            name="Maple Ridge",
            distance=Distance(6.5, "km"),
            elevation_gain_m=240,
            difficulty="easy",
        )

        trail.set_difficulty("hard")

        self.assertEqual(trail.difficulty, "hard")

    def test_invalid_difficulty_change_is_rejected(self):
        trail = Trail(
            trail_id=101,
            name="Maple Ridge",
            distance=Distance(6.5, "km"),
            elevation_gain_m=240,
            difficulty="easy",
        )

        with self.assertRaises(ValueError):
            trail.set_difficulty("impossible")

        self.assertEqual(trail.difficulty, "easy")

    def test_from_dict_populates_trail(self):
        data = {
            "id": 201,
            "name": "Lake View",
            "distance": 8.4,
            "unit": "km",
            "elevation_gain_m": 310,
            "difficulty": "hard",
        }

        trail = Trail.from_dict(data)

        self.assertEqual(trail.trail_id, 201)
        self.assertEqual(trail.name, "Lake View")
        self.assertEqual(trail.distance.magnitude, 8.4)
        self.assertEqual(trail.distance.unit, "km")
        self.assertEqual(trail.elevation_gain_m, 310.0)
        self.assertEqual(trail.difficulty, "hard")

    def test_from_dict_uses_default_unit_when_unit_is_missing(self):
        data = {
            "id": 201,
            "name": "Lake View",
            "distance": 8.4,
            "elevation_gain_m": 310,
            "difficulty": "hard",
        }

        trail = Trail.from_dict(data)

        self.assertEqual(trail.distance.unit, "km")

    def test_default_unit_change_affects_only_new_trails(self):
        first_data = {
            "id": 201,
            "name": "Lake View",
            "distance": 8.4,
            "elevation_gain_m": 310,
            "difficulty": "hard",
        }

        first_trail = Trail.from_dict(first_data)

        Trail.set_default_unit("mi")

        second_data = {
            "id": 202,
            "name": "Forest Path",
            "distance": 5.2,
            "elevation_gain_m": 120,
            "difficulty": "easy",
        }

        second_trail = Trail.from_dict(second_data)

        self.assertEqual(first_trail.distance.unit, "km")
        self.assertEqual(second_trail.distance.unit, "mi")

    def test_trails_with_same_id_compare_equal(self):
        first_trail = Trail(
            trail_id=101,
            name="Maple Ridge",
            distance=Distance(6.5, "km"),
            elevation_gain_m=240,
            difficulty="moderate",
        )

        second_trail = Trail(
            trail_id=101,
            name="Updated Maple Ridge",
            distance=Distance(7.0, "km"),
            elevation_gain_m=260,
            difficulty="hard",
        )

        self.assertEqual(first_trail, second_trail)

    def test_trails_with_different_ids_are_not_equal(self):
        first_trail = Trail(
            trail_id=101,
            name="Maple Ridge",
            distance=Distance(6.5, "km"),
            elevation_gain_m=240,
            difficulty="moderate",
        )

        second_trail = Trail(
            trail_id=102,
            name="Maple Ridge",
            distance=Distance(6.5, "km"),
            elevation_gain_m=240,
            difficulty="moderate",
        )

        self.assertNotEqual(first_trail, second_trail)


if __name__ == "__main__":
    unittest.main()