from django.db import IntegrityError
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from owners.tests.mock import (
    staff_doctor,
    staff_manager,
    staff_staff,
    superuser,
)
from ..models import Store
from .mock import store_1, store_2, store_3, store_4
from staffs.models import Staff


class StoreViewTest(APITestCase):
    def setUp(self) -> None:
        self.staff = Staff.objects.create(**staff_staff)
        self.doctor = Staff.objects.create(**staff_doctor)
        self.manager = Staff.objects.create(**staff_manager)
        self.super_user = Staff.objects.create_superuser(**superuser)

        self.token_staff = Token.objects.create(user=self.staff)
        self.token_doctor = Token.objects.create(user=self.doctor)
        self.token_manager = Token.objects.create(user=self.manager)
        self.token_super_user = Token.objects.create(user=self.super_user)

        Store.objects.bulk_create([Store(**store_1), Store(**store_2)])

    # Super user CRUD tests

    def test_super_user_can_create_a_store(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token " + self.token_super_user.key
        )
        response = self.client.post("/api/stores/", store_3)
        self.assertEquals(response.status_code, 201)

    def test_super_user_can_update_a_store(self):
        store = Store.objects.get(id=1)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token " + self.token_super_user.key
        )
        response = self.client.patch(f"/api/stores/{store.id}/")
        self.assertEquals(response.status_code, 200)

    def test_super_user_can_soft_delete_a_store(self):
        store = Store.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token " + self.token_super_user.key)
        response = self.client.patch(f"/api/stores/{store.id}/", data={"is_active": False})
        self.assertEquals(response.status_code, 200)

    def test_super_user_cant_create_a_store_with_wrong_state_choice(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token " + self.token_super_user.key
        )
        response = self.client.post("/api/stores/", store_4)
        self.assertEquals(response.status_code, 400)

    def test_only_authenticated_user_can_list_stores(self):
        response = self.client.get("/api/stores/")
        self.assertEquals(response.status_code, 401)

    def test_list_stores(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token " + self.token_super_user.key
        )
        response = self.client.get("/api/stores/")
        self.assertEquals(response.status_code, 200)

    # Manager CRUD tests - Only error tests

    def test_manager_cant_create_a_store(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token " + self.token_manager.key)
        response = self.client.post("/api/stores/", store_3)
        self.assertEquals(response.status_code, 403)

    def test_manager_cant_update_a_store(self):
        store = Store.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token " + self.token_manager.key)
        response = self.client.patch(f"/api/stores/{store.id}/", {"name": "Lojinha"})
        self.assertEquals(response.status_code, 403)

    # Staff CRUD tests - Only error tests

    def test_staff_cant_create_a_store(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token " + self.token_staff.key)
        response = self.client.post("/api/stores/", store_3)
        self.assertEquals(response.status_code, 403)

    def test_staff_cant_update_a_store(self):
        store = Store.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token " + self.token_staff.key)
        response = self.client.patch(f"/api/stores/{store.id}/", {"name": "Lojinha"})
        self.assertEquals(response.status_code, 403)

    # Doctor CRUD tests - Only error tests

    def test_doctor_cant_create_a_store(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token " + self.token_doctor.key)
        response = self.client.post("/api/stores/", store_3)
        self.assertEquals(response.status_code, 403)

    def test_doctor_cant_update_a_store(self):
        store = Store.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token " + self.token_doctor.key)
        response = self.client.patch(f"/api/stores/{store.id}/", {"name": "Lojinha"})
        self.assertEquals(response.status_code, 403)

    # List with and without authentication

    def test_only_authenticated_user_can_list_a_specific_store(self):
        store = Store.objects.get(id=1)
        response = self.client.get(f"/api/stores/{store.id}/")
        self.assertEquals(response.status_code, 401)

    def test_list_a_specific_stores(self):
        store = Store.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token " + self.token_staff.key)
        response = self.client.get(f"/api/stores/{store.id}/")
        self.assertEquals(response.status_code, 200)
