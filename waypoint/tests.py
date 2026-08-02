from django.test import TestCase
from django.urls import reverse


class Week11TemplateTests(TestCase):
    """Test the shared layout and temporary Week 11 catalog."""

    def test_catalog_renders_six_trails(self):
        response = self.client.get(reverse("catalog"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog.html")
        self.assertEqual(len(response.context["trails"]), 6)

    def test_catalog_formats_distances_and_badges(self):
        response = self.client.get(reverse("catalog"))

        self.assertContains(response, "5.3 km")
        self.assertContains(response, "14.9 km")
        self.assertContains(response, "HARD")
        self.assertContains(response, "CLOSED", count=2)
        self.assertContains(response, "Moderate", count=2)

    def test_catalog_numbers_rows_automatically(self):
        response = self.client.get(reverse("catalog"))
        page_html = response.content.decode()

        for number in range(1, 7):
            with self.subTest(number=number):
                self.assertIn(f"<td>{number}</td>", page_html)

    def test_shared_navigation_appears_on_every_page(self):
        page_names = ("home", "catalog", "search", "report")

        for page_name in page_names:
            with self.subTest(page_name=page_name):
                response = self.client.get(reverse(page_name))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, reverse("catalog"))
                self.assertContains(response, "Home")
                self.assertContains(response, "Catalog")
                self.assertContains(response, "Search")
                self.assertContains(response, "Report a trail")