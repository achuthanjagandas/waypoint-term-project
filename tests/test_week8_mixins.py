import unittest
from contextlib import redirect_stdout
from io import StringIO

from waypoint_core import (
    BackpackingRoute,
    DayHike,
    Distance,
    FakeTrail,
    GuidedDayHike,
    Trail,
    TrailRun,
    print_estimated_times,
)


class Week8MixinTests(unittest.TestCase):

    @staticmethod
    def create_guided_hike() -> GuidedDayHike:
        return GuidedDayHike(
            trail_id=10,
            name="Guided Ridge",
            distance=Distance(8, "km"),
            elevation_gain_m=600,
            difficulty="moderate",
            guide_name="Maya",
            group_size=10,
            pace_kmh=4,
            ratings=[4, 5, 3],
        )

    def test_guided_day_hike_is_a_day_hike(self):
        trail = self.create_guided_hike()

        self.assertIsInstance(trail, DayHike)
        self.assertIsInstance(trail, Trail)

    def test_guided_day_hike_stores_added_fields(self):
        trail = self.create_guided_hike()

        self.assertEqual(trail.guide_name, "Maya")
        self.assertEqual(trail.group_size, 10)

    def test_guided_hike_extends_day_hike_estimated_time(self):
        day_hike = DayHike(
            trail_id=1,
            name="Normal Hike",
            distance=Distance(8, "km"),
            elevation_gain_m=600,
            difficulty="moderate",
            pace_kmh=4,
        )
        guided_hike = self.create_guided_hike()

        self.assertAlmostEqual(
            guided_hike.estimated_time(),
            day_hike.estimated_time() + 0.5,
        )

    def test_guided_summary_extends_parent_summary(self):
        trail = self.create_guided_hike()

        summary = trail.summary()

        self.assertIn("day hike", summary)
        self.assertIn("Maya", summary)
        self.assertIn("10", summary)

    def test_guided_packing_list_extends_parent_list(self):
        trail = self.create_guided_hike()

        items = trail.packing_list()

        self.assertIn("water", items)
        self.assertIn("snacks", items)
        self.assertIn("booking confirmation", items)

    def test_elevation_mixin_calculates_grade(self):
        trail = GuidedDayHike(
            trail_id=11,
            name="Grade Trail",
            distance=Distance(2, "km"),
            elevation_gain_m=100,
            difficulty="easy",
            guide_name="Maya",
        )

        self.assertAlmostEqual(trail.grade_percent(), 5.0)

    def test_rating_mixin_calculates_average(self):
        trail = self.create_guided_hike()

        self.assertAlmostEqual(trail.average_rating, 4.0)

    def test_rating_mixin_rejects_invalid_rating(self):
        trail = self.create_guided_hike()

        with self.assertRaises(ValueError):
            trail.add_rating(6)

    def test_mro_uses_elevation_mixin_first(self):
        trail = self.create_guided_hike()
        mro = GuidedDayHike.__mro__

        self.assertEqual(trail.feature_label(), "elevation-aware")
        self.assertLess(
            mro.index(DayHike),
            mro.index(Trail),
        )
        self.assertEqual(mro[1].__name__, "ElevationMixin")
        self.assertEqual(mro[2].__name__, "RatingMixin")

    def test_polymorphic_loop_accepts_fake_trail(self):
        trails = [
            DayHike(
                trail_id=1,
                name="Day Trail",
                distance=Distance(4, "km"),
                elevation_gain_m=0,
                difficulty="easy",
                pace_kmh=4,
            ),
            BackpackingRoute(
                trail_id=2,
                name="Backpacking Trail",
                distance=Distance(6, "km"),
                elevation_gain_m=0,
                difficulty="moderate",
                days=2,
                pace_kmh=3,
            ),
            TrailRun(
                trail_id=3,
                name="Running Trail",
                distance=Distance(8, "km"),
                elevation_gain_m=0,
                difficulty="hard",
                pace_kmh=8,
            ),
            FakeTrail("Fake Trail", 1.25),
        ]

        output = StringIO()

        with redirect_stdout(output):
            print_estimated_times(trails)

        printed_text = output.getvalue()

        self.assertIn("Day Trail:", printed_text)
        self.assertIn("Backpacking Trail:", printed_text)
        self.assertIn("Running Trail:", printed_text)
        self.assertIn("Fake Trail: 1.25 hours", printed_text)
        self.assertNotIsInstance(trails[-1], Trail)


if __name__ == "__main__":
    unittest.main()