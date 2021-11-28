from collections import OrderedDict

import pytest
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from tires.models import TiresInfo
from users.models import User

pytestmark = pytest.mark.django_db


class TestUserTiresInfoView(APITestCase):

    url = "/api/v1/users/"

    @pytestmark
    def setUp(self) -> None:
        self.client = APIClient()

        # get login token
        self.username = "candycandy"
        self.password = "ASdfdsf3232@"
        self.user = User.objects.create(username=self.username)
        self.user.set_password(self.password)
        self.user.save()
        login_url = "/api/v1/users/login/"
        login_data = {"username": self.username, "password": self.password}
        self.jwt_token = self.client.post(
            login_url, login_data, format="json"
        ).data.get("access_token")
        self.car_data = {
            "username": self.user,
            "trim_id": 5000,
            "front_width": 225,
            "front_profile": 60,
            "front_rim": 16,
            "rear_width": 225,
            "rear_profile": 60,
            "rear_rim": 16,
        }
        TiresInfo.objects.create(**self.car_data)

    def test_get_users_tire_info(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        url = f"{self.url}{self.username}/"
        response = self.client.get(f"{url}", content_type="application/json")
        self.result = {
            "id": self.username,
            "trim_id": 5000,
            "front_width": 225,
            "front_profile": 60,
            "front_rim": 16,
            "rear_width": 225,
            "rear_profile": 60,
            "rear_rim": 16,
        }
        assert response.status_code == status.HTTP_200_OK
        assert response.data["results"][0] == OrderedDict(self.result)

    def test_get_users_tire_info_user_dosenotexist(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.jwt_token}")
        username = "konkon"
        url = f"{self.url}{username}/"
        response = self.client.get(f"{url}", content_type="application/json")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_users_tire_info_without_login_token(self):
        username = "candycandy"
        url = f"{self.url}{username}/"
        response = self.client.get(f"{url}", content_type="application/json")

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
