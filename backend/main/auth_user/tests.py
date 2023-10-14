# Create your tests here.
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username="testuser", email="testuser@example.com", password="testpassword"
        )
        self.valid_payload = {
            "username": "newusername",
            "email": "newemail@example.com",
            "password": "newpassword",
        }
        self.invalid_payload = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "newpassword",
        }

    def test_get_valid_user(self):
        response = self.client.get(reverse("get_user", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_user(self):
        response = self.client.get(reverse("get_user", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_valid_user(self):
        response = self.client.put(
            reverse("get_user", kwargs={"pk": self.user.pk}),
            data=self.valid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_update_invalid_user(self):
        response = self.client.put(
            reverse("get_user", kwargs={"pk": self.user.pk}),
            data=self.invalid_payload,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_valid_user(self):
        response = self.client.delete(reverse("get_user", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_invalid_user(self):
        response = self.client.delete(reverse("get_user", kwargs={"pk": 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
