from urllib import response

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from staffs.models import Staff
from store.models import Store

from .mock import doctor, manager, staff, store, superuser


class StaffViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.store = Store.objects.create(**store)

        cls.admin = Staff.objects.create_superuser(**superuser)
        cls.token_admin = Token.objects.create(user=cls.admin)

    def test_staff_creation_without_token(self):
        response = self.client.post(
            f"/api/stores/{self.store.id}/staffs/register/", data=manager
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # def test_manager_creation_by_superuser(self):
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

    #     response = self.client.post(
    #         f"/api/stores/{self.store.id}/staffs/register/", data=manager
    #     )

    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #     self.assertDictContainsSubset(response.data, manager)
