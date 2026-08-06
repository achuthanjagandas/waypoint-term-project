from decimal import Decimal

from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Park, Trail


class ParkModelTests(TestCase):
    """Test the database-backed Park model."""

    def test_string_representation_includes_name_and_region(self):
        park = Park(
            name="Test Park",
            region="Test Region",
        )

        self.assertEqual(str(park), "Test Park (Test Region)")


class TrailModelTests(TestCase):
    """Test Trail and Park model relationships."""

    @classmethod
    def setUpTestData(cls):
        cls.park = Park.objects.create(
            name="Cedar Lake Park",
            region="Central Ontario",
        )
        cls.trail = Trail.objects.create(
            name="Test Trail",
            park=cls.park,
            distance_km=Decimal("4.25"),
            elevation_gain=150,
            difficulty=Trail.Difficulty.EASY,
            is_open=True,
        )

    def test_string_representation_uses_trail_name(self):
        self.assertEqual(str(self.trail), "Test Trail")

    def test_reverse_relationship_returns_park_trails(self):
        trail_names = list(
            self.park.trails.values_list("name", flat=True)
        )

        self.assertEqual(trail_names, ["Test Trail"])

    def test_protect_prevents_deleting_park_with_trails(self):
        with self.assertRaises(ProtectedError):
            self.park.delete()


class TrailCatalogTests(TestCase):
    """Test the public database-driven Trail catalog."""

    @classmethod
    def setUpTestData(cls):
        cls.cedar = Park.objects.create(
            name="Cedar Lake Park",
            region="Central Ontario",
        )
        cls.greenwood = Park.objects.create(
            name="Greenwood Forest Park",
            region="Eastern Ontario",
        )
        cls.northern = Park.objects.create(
            name="Northern Peaks Park",
            region="Northern Ontario",
        )

        Trail.objects.create(
            name="Lake View Trail",
            park=cls.cedar,
            distance_km=Decimal("5.25"),
            elevation_gain=120,
            difficulty=Trail.Difficulty.EASY,
            is_open=True,
        )
        Trail.objects.create(
            name="Forest Ridge",
            park=cls.greenwood,
            distance_km=Decimal("8.44"),
            elevation_gain=340,
            difficulty=Trail.Difficulty.MODERATE,
            is_open=True,
        )
        Trail.objects.create(
            name="Summit Loop",
            park=cls.northern,
            distance_km=Decimal("12.08"),
            elevation_gain=780,
            difficulty=Trail.Difficulty.EXPERT,
            is_open=True,
        )
        Trail.objects.create(
            name="River Path",
            park=cls.cedar,
            distance_km=Decimal("3.76"),
            elevation_gain=45,
            difficulty=Trail.Difficulty.EASY,
            is_open=False,
        )
        Trail.objects.create(
            name="Pine Valley Route",
            park=cls.greenwood,
            distance_km=Decimal("9.63"),
            elevation_gain=410,
            difficulty=Trail.Difficulty.MODERATE,
            is_open=True,
        )
        Trail.objects.create(
            name="Granite Peak Trail",
            park=cls.northern,
            distance_km=Decimal("14.91"),
            elevation_gain=960,
            difficulty=Trail.Difficulty.EXPERT,
            is_open=False,
        )

    def test_catalog_route_is_mounted_under_trails(self):
        self.assertEqual(reverse("catalog"), "/trails/")

    def test_catalog_displays_only_open_trails_ordered_by_distance(self):
        response = self.client.get(reverse("catalog"))

        trail_names = list(
            response.context["trails"].values_list(
                "name",
                flat=True,
            )
        )

        self.assertEqual(
            trail_names,
            [
                "Lake View Trail",
                "Forest Ridge",
                "Pine Valley Route",
                "Summit Loop",
            ],
        )

        self.assertNotContains(response, "River Path")
        self.assertNotContains(response, "Granite Peak Trail")

    def test_catalog_reuses_shared_catalog_template(self):
        response = self.client.get(reverse("catalog"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog.html")

    def test_catalog_formats_model_values_and_badges(self):
        response = self.client.get(reverse("catalog"))

        self.assertContains(response, "5.3 km")
        self.assertContains(response, "12.1 km")
        self.assertContains(response, "HARD")
        self.assertContains(response, "Moderate", count=2)
        self.assertNotContains(response, "CLOSED")

    def test_catalog_numbers_only_visible_trails(self):
        response = self.client.get(reverse("catalog"))
        page_html = response.content.decode()

        for number in range(1, 5):
            with self.subTest(number=number):
                self.assertIn(f"<td>{number}</td>", page_html)

        self.assertNotIn("<td>5</td>", page_html)

    def test_catalog_displays_each_open_trails_park(self):
        response = self.client.get(reverse("catalog"))

        self.assertContains(response, "Cedar Lake Park")
        self.assertContains(response, "Greenwood Forest Park")
        self.assertContains(response, "Northern Peaks Park")
        self.assertContains(response, "Central Ontario")
        self.assertContains(response, "Eastern Ontario")
        self.assertContains(response, "Northern Ontario")

    def test_filtering_by_park_returns_correct_open_trails(self):
        response = self.client.get(
            reverse("catalog"),
            {"park": self.greenwood.pk},
        )

        trail_names = list(
            response.context["trails"].values_list(
                "name",
                flat=True,
            )
        )

        self.assertEqual(
            trail_names,
            [
                "Forest Ridge",
                "Pine Valley Route",
            ],
        )
        self.assertEqual(
            response.context["selected_park"],
            self.greenwood,
        )
        self.assertNotContains(response, "Lake View Trail")
        self.assertNotContains(response, "Summit Loop")

    def test_invalid_park_filter_does_not_crash(self):
        response = self.client.get(
            reverse("catalog"),
            {"park": "not-a-number"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.context["selected_park"])
        self.assertEqual(response.context["trails"].count(), 4)