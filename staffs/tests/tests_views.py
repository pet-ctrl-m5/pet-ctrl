from urllib import response

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from staffs.models import Staff
from store.models import Store

from .mock import (
    created_doctor,
    created_manager,
    created_staff,
    doctor,
    manager,
    staff,
    store,
    superuser,
)


class StaffViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.store = Store.objects.create(**store)

        cls.admin = Staff.objects.create_superuser(**superuser)
        cls.manager = Staff.objects.create(**created_manager)
        cls.staff = Staff.objects.create(**created_staff)
        cls.doctor = Staff.objects.create(**created_doctor)

        cls.token_admin = Token.objects.create(user=cls.admin)
        cls.token_manager = Token.objects.create(user=cls.manager)
        cls.token_staff = Token.objects.create(user=cls.staff)
        cls.token_doctor = Token.objects.create(user=cls.doctor)

    def test_staff_creation_without_token(self):
        response = self.client.post(
            f"/api/stores/{self.store.id}/staffs/register/", data=manager
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_manager_creation_by_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.post(
            f"/api/stores/{self.store.id}/staffs/register/", data=manager
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("is_superuser", response.data)
        self.assertIn("is_manager", response.data)
        self.assertIn("is_staff", response.data)
        self.assertIn("is_doctor", response.data)
        self.assertIn("date_joined", response.data)
        self.assertIn("store", response.data)

        self.assertEqual(False, response.data["is_superuser"])
        self.assertEqual(True, response.data["is_active"])
        self.assertEqual(self.store.id, response.data["store"])

    def test_manager_creation_by_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.post(
            f"/api/stores/{self.store.id}/staffs/register/", data=manager
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertIn("id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("is_superuser", response.data)
        self.assertIn("is_manager", response.data)
        self.assertIn("is_staff", response.data)
        self.assertIn("is_doctor", response.data)
        self.assertIn("date_joined", response.data)
        self.assertIn("store", response.data)

        self.assertEqual(False, response.data["is_superuser"])
        self.assertEqual(True, response.data["is_active"])
        self.assertEqual(self.store.id, response.data["store"])

    def test_manager_creation_by_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.post(
            f"/api/stores/{self.store.id}/staffs/register/", data=manager
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_creation_by_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.post(
            f"/api/stores/{self.store.id}/staffs/register/", data=manager
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_cannot_update_superuser(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.patch(
            f"/api/staffs/{self.admin.id}/", data=staff
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superuser_can_update_manager(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.patch(
            f"/api/staffs/{self.manager.id}/", data=manager
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("is_superuser", response.data)
        self.assertIn("is_manager", response.data)
        self.assertIn("is_staff", response.data)
        self.assertIn("is_doctor", response.data)
        self.assertIn("date_joined", response.data)
        self.assertIn("store", response.data)

    def test_update_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.patch(
            f"/api/staffs/{self.staff.id}/", data=staff
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("username", response.data)
        self.assertIn("first_name", response.data)
        self.assertIn("last_name", response.data)
        self.assertIn("is_active", response.data)
        self.assertIn("is_superuser", response.data)
        self.assertIn("is_manager", response.data)
        self.assertIn("is_staff", response.data)
        self.assertIn("is_doctor", response.data)
        self.assertIn("date_joined", response.data)
        self.assertIn("store", response.data)

    def test_update_without_token(self):

        response = self.client.patch(
            f"/api/staffs/{self.manager.id}/", data=manager
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.patch(
            f"/api/staffs/{self.manager.id}/", data=manager
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_list_staffs(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.get(f"/api/staffs/")

        staffs = Staff.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(staffs), response.data["count"])
