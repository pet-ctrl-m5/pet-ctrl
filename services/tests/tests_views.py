from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from services.models import Service
from services.serializers import ServiceSerializer
from staffs.models import Staff

from .mocks import (
    admin,
    doctor,
    manager,
    service_1,
    service_2,
    service_2_price,
    service_2_update,
    staff,
)


class ServiceViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.admin = Staff.objects.create_superuser(**admin)
        cls.staff = Staff.objects.create(**staff)
        cls.manager = Staff.objects.create(**manager)
        cls.doctor = Staff.objects.create(**doctor)

        cls.token_admin = Token.objects.create(user=cls.admin)
        cls.token_staff = Token.objects.create(user=cls.staff)
        cls.token_manager = Token.objects.create(user=cls.manager)
        cls.token_doctor = Token.objects.create(user=cls.doctor)

        cls.service_2 = Service.objects.create(**service_2)

    def test_service_creation_without_token(self):
        response = self.client.post("/api/services/", data=service_1)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_service_creation_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.post("/api/services/", data=service_1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data)
        self.assertIn("name", response.data)
        self.assertIn("category", response.data)
        self.assertIn("price", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_service_creation_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )
        response = self.client.post("/api/services/", data=service_1)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data)
        self.assertIn("name", response.data)
        self.assertIn("category", response.data)
        self.assertIn("price", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_service_creation_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")
        response = self.client.post("/api/services/", data=service_1)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_service_creation_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )
        response = self.client.post("/api/services/", data=service_1)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_create_service_with_same_name(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.post("/api/services/", data=service_2)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_service_without_token(self):
        response = self.client.patch(f"/api/services/{self.service_2.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_service_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.patch(
            f"/api/services/{self.service_2.id}/", data=service_2_update
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("name", response.data)
        self.assertIn("category", response.data)
        self.assertIn("price", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

        self.assertDictContainsSubset(service_2_update, response.data)

    def test_update_service_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )
        response = self.client.patch(
            f"/api/services/{self.service_2.id}/", data=service_2_update
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("name", response.data)
        self.assertIn("category", response.data)
        self.assertIn("price", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

        self.assertDictContainsSubset(service_2_update, response.data)

    def test_update_service_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")
        response = self.client.patch(
            f"/api/services/{self.service_2.id}/", data=service_2_update
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_service_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )
        response = self.client.patch(
            f"/api/services/{self.service_2.id}/", data=service_2_update
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_price_update_should_create_a_new_service(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.patch(
            f"/api/services/{self.service_2.id}/", data=service_2_price
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(self.service_2.id, response.data["id"])

        self.assertEqual(service_2_price["name"], response.data["name"])
        self.assertEqual(
            service_2_price["category"], response.data["category"]
        )

        self.assertIn("id", response.data)
        self.assertIn("name", response.data)
        self.assertIn("category", response.data)
        self.assertIn("price", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)

    def test_service_retrieve_without_token(self):
        response = self.client.get(f"/api/services/{self.service_2.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_service_retrieve_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.get(f"/api/services/{self.service_2.id}/")

        service = ServiceSerializer(instance=self.service_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(service.data, response.data)

    def test_service_retrieve_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )
        response = self.client.get(f"/api/services/{self.service_2.id}/")

        service = ServiceSerializer(instance=self.service_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(service.data, response.data)

    def test_service_retrieve_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")
        response = self.client.get(f"/api/services/{self.service_2.id}/")

        service = ServiceSerializer(instance=self.service_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(service.data, response.data)

    def test_service_retrieve_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )
        response = self.client.get(f"/api/services/{self.service_2.id}/")

        service = ServiceSerializer(instance=self.service_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(service.data, response.data)
