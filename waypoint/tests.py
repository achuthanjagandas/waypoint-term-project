from django.test import TestCase
from django.urls import reverse


class SharedTemplateTests(TestCase):
    """Test shared navigation across the project pages."""

    def test_shared_navigation_appears_on_every_page(self):
        page_names = (
            "home",
            "catalog",
            "search",
            "report",
        )

        for page_name in page_names:
            with self.subTest(page_name=page_name):
                response = self.client.get(reverse(page_name))

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, reverse("catalog"))
                self.assertContains(response, "Home")
                self.assertContains(response, "Catalog")
                self.assertContains(response, "Search")
                self.assertContains(response, "Report a trail")