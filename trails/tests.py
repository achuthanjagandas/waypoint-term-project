from decimal import Decimal

from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.urls import reverse

from .models import Park, Trail


class ParkModelTests(TestCase):
    """Test the Park database model."""

    def test_string_representation_includes_name_and_region(self):
        park = Park.objects.create(
            name="Test Park",
            region="Test Region",
        )

        self.assertEqual(
            str(park),
            "Test Park (Test Region)",
        )


class TrailModelTests(TestCase):
    """Test Trail and Park model relationships."""

    @classmethod
    def setUpTestData(cls):
        cls.park = Park.objects.create(
            name="Cedar Lake Park",
            region="Central Ontario",
        )

        cls.trail = Trail.objects.create(
            park=cls.park,
            name="Lake View Trail",
            distance_km=Decimal("5.25"),
            elevation_gain=120,
            difficulty=Trail.Difficulty.EASY,
            is_open=True,
        )

    def test_trail_string_representation_returns_name(self):
        self.assertEqual(
            str(self.trail),
            "Lake View Trail",
        )

    def test_park_relationship_is_required(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Trail.objects.create(
                    name="Trail Without Park",
                    distance_km=Decimal("2.50"),
                    elevation_gain=75,
                    difficulty=Trail.Difficulty.EASY,
                    is_open=True,
                )

    def test_park_reverse_relationship_returns_trails(self):
        related_trails = list(self.park.trails.all())

        self.assertEqual(
            related_trails,
            [self.trail],
        )

    def test_protected_park_cannot_be_deleted(self):
        with self.assertRaises(ProtectedError):
            self.park.delete()


class TrailCatalogTests(TestCase):
    """Test the database-backed Trail catalog and detail pages."""

    @classmethod
    def setUpTestData(cls):
        cls.cedar_park = Park.objects.create(
            name="Cedar Lake Park",
            region="Central Ontario",
        )

        cls.greenwood_park = Park.objects.create(
            name="Greenwood Forest Park",
            region="Eastern Ontario",
        )

        cls.northern_park = Park.objects.create(
            name="Northern Peaks Park",
            region="Northern Ontario",
        )

        cls.lake_view = Trail.objects.create(
            park=cls.cedar_park,
            name="Lake View Trail",
            distance_km=Decimal("5.25"),
            elevation_gain=120,
            difficulty=Trail.Difficulty.EASY,
            is_open=True,
        )

        cls.forest_ridge = Trail.objects.create(
            park=cls.greenwood_park,
            name="Forest Ridge",
            distance_km=Decimal("8.44"),
            elevation_gain=340,
            difficulty=Trail.Difficulty.MODERATE,
            is_open=True,
        )

        cls.pine_valley = Trail.objects.create(
            park=cls.greenwood_park,
            name="Pine Valley Route",
            distance_km=Decimal("9.63"),
            elevation_gain=410,
            difficulty=Trail.Difficulty.MODERATE,
            is_open=True,
        )

        cls.summit_loop = Trail.objects.create(
            park=cls.northern_park,
            name="Summit Loop",
            distance_km=Decimal("12.08"),
            elevation_gain=780,
            difficulty=Trail.Difficulty.EXPERT,
            is_open=True,
        )

        cls.river_path = Trail.objects.create(
            park=cls.cedar_park,
            name="River Path",
            distance_km=Decimal("3.76"),
            elevation_gain=45,
            difficulty=Trail.Difficulty.EASY,
            is_open=False,
        )

        cls.granite_peak = Trail.objects.create(
            park=cls.northern_park,
            name="Granite Peak Trail",
            distance_km=Decimal("14.91"),
            elevation_gain=960,
            difficulty=Trail.Difficulty.EXPERT,
            is_open=False,
        )

    def test_catalog_route_is_mounted_under_trails(self):
        self.assertEqual(
            reverse("catalog"),
            "/trails/",
        )

    def test_catalog_reuses_shared_catalog_template(self):
        response = self.client.get(reverse("catalog"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "catalog.html",
        )

    def test_catalog_displays_each_open_trails_park(self):
        response = self.client.get(reverse("catalog"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response,
            self.cedar_park.name,
        )
        self.assertContains(
            response,
            self.cedar_park.region,
        )

        self.assertContains(
            response,
            self.greenwood_park.name,
        )
        self.assertContains(
            response,
            self.greenwood_park.region,
        )

        self.assertContains(
            response,
            self.northern_park.name,
        )
        self.assertContains(
            response,
            self.northern_park.region,
        )

    def test_catalog_open_trails_query_is_ordered_by_distance(self):
        response = self.client.get(reverse("catalog"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog.html")

        displayed_trails = list(response.context["trails"])

        self.assertEqual(
            displayed_trails,
            [
                self.lake_view,
                self.forest_ridge,
                self.pine_valley,
                self.summit_loop,
            ],
        )

        self.assertNotContains(
            response,
            self.river_path.name,
        )
        self.assertNotContains(
            response,
            self.granite_peak.name,
        )

    def test_catalog_formats_model_values_and_badges(self):
        response = self.client.get(reverse("catalog"))

        self.assertContains(
            response,
            "5.3 km",
        )
        self.assertContains(
            response,
            "120 m",
        )
        self.assertContains(
            response,
            "Easy",
        )
        self.assertContains(
            response,
            "Moderate",
        )
        self.assertContains(
            response,
            "HARD",
        )
        self.assertNotContains(
            response,
            "CLOSED",
        )

    def test_catalog_numbers_only_visible_trails(self):
        response = self.client.get(reverse("catalog"))
        page_html = response.content.decode()

        for number in range(1, 5):
            with self.subTest(number=number):
                self.assertIn(
                    f"<td>{number}</td>",
                    page_html,
                )

        self.assertNotIn(
            "<td>5</td>",
            page_html,
        )

    def test_catalog_filters_open_trails_by_park(self):
        response = self.client.get(
            reverse("catalog"),
            {"park": self.greenwood_park.id},
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertEqual(
            response.context["selected_park"],
            self.greenwood_park,
        )

        displayed_trails = list(
            response.context["trails"]
        )

        self.assertEqual(
            displayed_trails,
            [
                self.forest_ridge,
                self.pine_valley,
            ],
        )

        self.assertContains(
            response,
            self.greenwood_park.name,
        )
        self.assertContains(
            response,
            self.greenwood_park.region,
        )
        self.assertContains(
            response,
            self.forest_ridge.name,
        )
        self.assertContains(
            response,
            self.pine_valley.name,
        )

        self.assertNotContains(
            response,
            self.lake_view.name,
        )
        self.assertNotContains(
            response,
            self.summit_loop.name,
        )

    def test_catalog_invalid_park_value_uses_all_parks(self):
        response = self.client.get(
            reverse("catalog"),
            {"park": "not-a-valid-id"},
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertIsNone(
            response.context["selected_park"]
        )
        self.assertEqual(
            response.context["trails"].count(),
            4,
        )

        self.assertContains(
            response,
            self.lake_view.name,
        )
        self.assertContains(
            response,
            self.forest_ridge.name,
        )
        self.assertContains(
            response,
            self.pine_valley.name,
        )
        self.assertContains(
            response,
            self.summit_loop.name,
        )

    def test_trail_detail_displays_existing_trail(self):
        response = self.client.get(
            reverse(
                "trail_detail",
                args=[self.lake_view.id],
            )
        )

        self.assertEqual(
            response.status_code,
            200,
        )
        self.assertTemplateUsed(
            response,
            "trail_detail.html",
        )
        self.assertEqual(
            response.context["trail"],
            self.lake_view,
        )

        self.assertContains(
            response,
            self.lake_view.name,
        )
        self.assertContains(
            response,
            self.lake_view.park.name,
        )
        self.assertContains(
            response,
            self.lake_view.park.region,
        )
        self.assertContains(
            response,
            "5.3 km",
        )
        self.assertContains(
            response,
            "Open to visitors",
        )

    def test_trail_detail_returns_404_for_missing_trail(self):
        response = self.client.get(
            reverse(
                "trail_detail",
                args=[999999],
            )
        )

        self.assertEqual(
            response.status_code,
            404,
        )