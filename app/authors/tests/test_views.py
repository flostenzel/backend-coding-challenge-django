from authors.models import Author
from rest_framework import status

from app.tests.utils import APIViewTest


class TestSignupView(APIViewTest):
    url = "/authors/signup/"
    auth = False

    def test_successful_signup(self):
        data = {
            "username": "testUsername",
            "password": "paSsw0rd",
        }
        self.assertFalse(Author.objects.all())
        response = self.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Author.objects.all())


class TestLoginView(APIViewTest):
    url = "/authors/login/"

    def test_successful_login(self):
        data = {"username": "testUsername", "password": "paSsw0rd"}
        self.auth_user.username = data["username"]
        self.auth_user.set_password(data["password"])
        self.auth_user.save()

        response = self.post(self.url, data, auth=None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json["token"], self.token.key)

    def test_unsuccessful_login(self):
        data = {"username": "testUsername", "password": "paSsw0rd"}
        response = self.post(self.url, data, expect_errors=True)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json["non_field_errors"][0],
            "Unable to log in with provided credentials.",
        )


class TestLogoutView(APIViewTest):
    url = "/authors/logout/"

    def test_logout(self):
        response = self.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
