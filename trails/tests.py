from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .models import Trail


class TrailModelTests(TestCase):
    """Test the database-backed Trail model."""

    def test_string_representation_uses_trail_name(self):
        trail = Trail(
            name="Test Trail",
            distance_km=Decimal("4.25"),
            elevation_gain=150,
            difficulty=Trail.Difficulty.EASY,
            is_open=True,
        )

        self.assertEqual(str(trail), "Test Trail")


class TrailCatalogTests(TestCase):
    """Test the public database-driven trail catalog."""

    @classmethod
    def setUpTestData(cls):
        Trail.objects.create(
            name="Lake View Trail",
            distance_km=Decimal("5.25"),
            elevation_gain=120,
            difficulty=Trail.Difficulty.EASY,
            is_open=True,
        )
        Trail.objects.create(
            name="Forest Ridge",
            distance_km=Decimal("8.44"),
            elevation_gain=340,
            difficulty=Trail.Difficulty.MODERATE,
            is_open=True,
        )
        Trail.objects.create(
            name="Summit Loop",
            distance_km=Decimal("12.08"),
            elevation_gain=780,
            difficulty=Trail.Difficulty.EXPERT,
            is_open=True,
        )
        Trail.objects.create(
            name="River Path",
            distance_km=Decimal("3.76"),
            elevation_gain=45,
            difficulty=Trail.Difficulty.EASY,
            is_open=False,
        )
        Trail.objects.create(
            name="Pine Valley Route",
            distance_km=Decimal("9.63"),
            elevation_gain=410,
            difficulty=Trail.Difficulty.MODERATE,
            is_open=True,
        )
        Trail.objects.create(
            name="Granite Peak Trail",
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
            response.context["trails"].values_list("name", flat=True)
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

    def test_catalog_reuses_week11_template(self):
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