from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class SearchAPITests(TestCase):

    def setUp(self):
        self.url = reverse("search-decisions")

    def test_valid_search_request(self):
        response = self.client.post(
            self.url,
            {
                "query": "Haksız işten çıkarılma ile ilgili kararlar",
                "top_k": 5,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["top_k"], 5)

    def test_short_query_is_rejected(self):
        response = self.client.post(
            self.url,
            {"query": "iş", "top_k": 5},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_top_k_is_rejected(self):
        response = self.client.post(
            self.url,
            {
                "query": "İş sözleşmesinin feshi hakkında kararlar",
                "top_k": 30,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

