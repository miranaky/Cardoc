import pytest
from django.test import TestCase
from model_bakery import baker
from rest_framework.test import APIClient, APITestCase

from tires.models import TiresInfo
from tires.views import tire_size
from users.models import User

pytestmark = pytest.mark.django_db


def test_tire_size():
    assert tire_size("225/60R16") == ("225", "60", "16")
    assert tire_size("215/60R17") == ("215", "60", "17")
    assert tire_size("abcde") == (None, None, None)


# --------------------------------------


class TestTireModels(TestCase):
    """Test Tire Model"""

    def setUp(self) -> None:
        if isinstance(TiresInfo, type):
            self.model = baker.make(TiresInfo)

    def test_create_models(self):
        assert self.model


# --------------------------------------


class TestCreateTiresInfoView(APITestCase):
    """Test CreateTiresInfo View"""

    url = "/api/v1/tires/"

    def setUp(self) -> None:
        self.client = APIClient()
        # create dummy user
        self.password = "ASdfdsf3232@"
        self.user = User.objects.create(username="candycandy")
        self.user.set_password(self.password)
        self.user.save()
        login_url = "/api/v1/users/login/"
        login_data = {"username": self.user.username, "password": self.password}
        self.jwt_token = self.client.post(
            login_url, login_data, format="json"
        ).data.get("access_token")

    def test_create_single_tires_info(self):
        input_json = [
            {
                "id": "candycandy",
                "trimId": 5000,
            }
        ]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        res = self.client.post(self.url, data=input_json, format="json")

        assert res.status_code == 200

    def test_create_single_tires_info_without_token(self):
        input_json = [
            {
                "id": "candycandy",
                "trimId": 5000,
            }
        ]

        res = self.client.post(self.url, data=input_json, format="json")
        assert res.status_code == 401

    def test_create_single_tires_user_doesnotexist(self):
        input_json = [
            {
                "id": "sugarsugar",
                "trimId": 5000,
            }
        ]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        res = self.client.post(self.url, data=input_json, format="json")

        assert res.status_code == 400

    def test_create_multi_tires_info(self):
        input_json = [
            {
                "id": "candycandy",
                "trimId": 5000,
            },
            {
                "id": "candycandy",
                "trimId": 8000,
            },
            {
                "id": "candycandy",
                "trimId": 11000,
            },
        ]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        res = self.client.post(self.url, data=input_json, format="json")

        assert res.status_code == 200

    def test_create_multi_tires_info_wrong_input(self):
        input_json = [
            {
                "id": "candycandy",
                "trimId": 5000,
            },
            {
                "id": "candycandy",
                "trimId": 8000,
            },
            {
                "id": "sugarsugar",
                "trimId": 11000,
            },
        ]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        res = self.client.post(self.url, data=input_json, format="json")

        assert res.status_code == 400

    def test_create_multi_tires_info_wrong_input2(self):
        input_json = [
            {
                "id": "candycandy",
                "trimId": 5000,
            },
            {
                "id": "candycandy",
                "trimId": 8000,
            },
            {
                "id": "candycandy",
                "trimId": 112312000,
            },
        ]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        res = self.client.post(self.url, data=input_json, format="json")

        assert res.status_code == 400
