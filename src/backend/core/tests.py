from django.test import TestCase
from django.urls import reverse


class HealthTest(TestCase):
    def test_health_endpoint(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
