import json

from django.test import TestCase
from model_bakery import baker
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from users.models import User


class TestUserModels(TestCase):
    """Test User Model"""

    def setUp(self) -> None:
        if isinstance(User, type):
            self.model = baker.make(User)

    def test_create_models(self):
        assert self.model


# --------------------------------------


class TestUserViews(APITestCase):
    """Test User Views"""

    def setUp(self) -> None:
        self.client = APIClient()
        # create dummy user
        self.password = "ASdfdsf3232@"
        self.user = User.objects.create(username="test_user")
        self.user.set_password(self.password)
        self.user.save()

    def test_create_new_account(self):
        url = "/api/v1/users/"
        new_user_data = json.dumps(
            {
                "username": "candycandy",
                "password": "ASdfdsf3232@",
            }
        )
        res = self.client.post(url, new_user_data, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        assert res.data.get("access_token") is not None

    def test_login_account(self):
        url = "/api/v1/users/login/"
        login_data = json.dumps(
            {"username": self.user.username, "password": self.password}
        )
        res = self.client.post(url, login_data, content_type="application/json")
        assert res.status_code == status.HTTP_200_OK
        assert res.data.get("access_token") is not None
