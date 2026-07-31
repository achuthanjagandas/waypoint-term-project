import unittest

from waypoint_core import Distance


class DistanceOperatorTests(unittest.TestCase):

    def test_addition_with_same_units(self):
        result = Distance(3, "km") + Distance(2, "km")

        self.assertEqual(result, Distance(5, "km"))
        self.assertEqual(result.unit, "km")

    def test_addition_automatically_converts_mixed_units(self):
        result = Distance(5, "km") + Distance(1, "mi")

        expected = (
            5
            + Distance(1, "mi").convert("km").magnitude
        )

        self.assertEqual(result.unit, "km")
        self.assertAlmostEqual(
            result.magnitude,
            expected,
            places=5,
        )

    def test_addition_result_uses_left_hand_unit(self):
        result = Distance(1, "mi") + Distance(1, "km")

        self.assertEqual(result.unit, "mi")

    def test_subtraction_with_same_units(self):
        result = Distance(5, "km") - Distance(2, "km")

        self.assertEqual(result, Distance(3, "km"))

    def test_subtraction_automatically_converts_mixed_units(self):
        result = Distance(10, "km") - Distance(2, "mi")

        expected = (
            10
            - Distance(2, "mi").convert("km").magnitude
        )

        self.assertEqual(result.unit, "km")
        self.assertAlmostEqual(
            result.magnitude,
            expected,
            places=5,
        )

    def test_subtraction_rejects_negative_result(self):
        with self.assertRaises(ValueError):
            Distance(2, "km") - Distance(3, "km")

    def test_equal_distances_with_same_units(self):
        self.assertEqual(
            Distance(5, "km"),
            Distance(5, "km"),
        )

    def test_equal_distances_with_mixed_units(self):
        miles = Distance(1, "mi")
        kilometres = miles.convert("km")

        self.assertEqual(miles, kilometres)

    def test_different_distances_are_not_equal(self):
        self.assertNotEqual(
            Distance(5, "km"),
            Distance(6, "km"),
        )

    def test_less_than_with_mixed_units(self):
        self.assertLess(
            Distance(1, "km"),
            Distance(1, "mi"),
        )

    def test_greater_than_with_mixed_units(self):
        self.assertGreater(
            Distance(1, "mi"),
            Distance(1, "km"),
        )

    def test_distances_can_be_sorted(self):
        distances = [
            Distance(5, "km"),
            Distance(1, "mi"),
            Distance(3, "km"),
        ]

        sorted_distances = sorted(distances)

        self.assertEqual(
            sorted_distances,
            [
                Distance(1, "mi"),
                Distance(3, "km"),
                Distance(5, "km"),
            ],
        )

    def test_string_representation(self):
        distance = Distance(5, "km")

        self.assertEqual(str(distance), "5.00 km")

    def test_developer_representation(self):
        distance = Distance(5, "km")

        self.assertEqual(
            repr(distance),
            "Distance(magnitude=5.0, unit='km')",
        )


if __name__ == "__main__":
    unittest.main()