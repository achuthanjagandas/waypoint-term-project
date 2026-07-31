import unittest

from waypoint_core import DayHike, Distance, Itinerary, Trail


class ItineraryTests(unittest.TestCase):

    @staticmethod
    def create_trail(
        trail_id: int,
        name: str,
        magnitude: float,
        unit: str = "km",
    ) -> Trail:
        return DayHike(
            trail_id=trail_id,
            name=name,
            distance=Distance(magnitude, unit),
            elevation_gain_m=100,
            difficulty="moderate",
        )

    def test_new_itinerary_is_empty(self):
        itinerary = Itinerary()

        self.assertEqual(itinerary.trails, ())

    def test_add_trail_preserves_order(self):
        first_trail = self.create_trail(1, "Lake Trail", 2)
        second_trail = self.create_trail(2, "Forest Trail", 3)

        itinerary = Itinerary()
        itinerary.add_trail(first_trail)
        itinerary.add_trail(second_trail)

        self.assertEqual(
            itinerary.trails,
            (first_trail, second_trail),
        )

    def test_non_trail_object_is_rejected(self):
        itinerary = Itinerary()

        with self.assertRaises(TypeError):
            itinerary.add_trail("Lake Trail")

    def test_three_trails_report_correct_total_distance(self):
        itinerary = Itinerary(
            [
                self.create_trail(1, "Lake Trail", 2.5),
                self.create_trail(2, "Forest Trail", 3.5),
                self.create_trail(3, "Hill Trail", 4.0),
            ]
        )

        total = itinerary.total_distance("km")

        self.assertEqual(total.unit, "km")
        self.assertAlmostEqual(total.magnitude, 10.0)

    def test_total_distance_converts_mixed_units(self):
        itinerary = Itinerary(
            [
                self.create_trail(1, "Lake Trail", 5, "km"),
                self.create_trail(2, "Forest Trail", 2, "mi"),
            ]
        )

        total = itinerary.total_distance("km")

        expected_total = 5 + Distance(2, "mi").convert("km").magnitude

        self.assertAlmostEqual(
            total.magnitude,
            expected_total,
            places=5,
        )

    def test_adding_to_one_itinerary_does_not_change_another(self):
        first_itinerary = Itinerary()
        second_itinerary = Itinerary()

        trail = self.create_trail(1, "Lake Trail", 5)
        first_itinerary.add_trail(trail)

        self.assertEqual(len(first_itinerary.trails), 1)
        self.assertEqual(len(second_itinerary.trails), 0)

    def test_constructor_copies_supplied_trails(self):
        original_list = [
            self.create_trail(1, "Lake Trail", 5),
        ]

        itinerary = Itinerary(original_list)

        original_list.append(
            self.create_trail(2, "Forest Trail", 3)
        )

        self.assertEqual(len(original_list), 2)
        self.assertEqual(len(itinerary.trails), 1)


if __name__ == "__main__":
    unittest.main()