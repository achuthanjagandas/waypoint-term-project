import unittest

from waypoint_core import Distance


class DistanceTests(unittest.TestCase):

    def test_distance_stores_magnitude_and_unit(self):
        distance = Distance(5, "km")

        self.assertEqual(distance.magnitude, 5.0)
        self.assertEqual(distance.unit, "km")

    def test_negative_distance_is_rejected(self):
        with self.assertRaises(ValueError):
            Distance(-1, "km")

    def test_invalid_unit_is_rejected(self):
        with self.assertRaises(ValueError):
            Distance(5, "m")

    def test_magnitude_is_read_only(self):
        distance = Distance(5, "km")

        with self.assertRaises(AttributeError):
            distance.magnitude = 10

    def test_unit_is_read_only(self):
        distance = Distance(5, "km")

        with self.assertRaises(AttributeError):
            distance.unit = "mi"

    def test_kilometres_convert_to_miles(self):
        distance = Distance(10, "km")
        converted = distance.convert("mi")

        self.assertEqual(converted.unit, "mi")
        self.assertAlmostEqual(converted.magnitude, 6.21371, places=5)

    def test_conversion_round_trip(self):
        original = Distance(10, "km")

        converted_to_miles = original.convert("mi")
        converted_back = converted_to_miles.convert("km")

        self.assertAlmostEqual(
            converted_back.magnitude,
            original.magnitude,
            places=5,
        )


if __name__ == "__main__":
    unittest.main()