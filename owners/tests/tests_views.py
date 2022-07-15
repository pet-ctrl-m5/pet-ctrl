from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from ..models import Owner
from staffs.models import Staff
from .mock import staff_staff, staff_doctor, staff_manager, owner_1, owner_2, owner_3, superuser


class OwnerViewTest(APITestCase):
    def setUp(self) -> None:
        self.staff = Staff.objects.create(**staff_staff)
        self.doctor = Staff.objects.create(**staff_doctor)
        self.manager = Staff.objects.create(**staff_manager)

        self.super_user = Staff.objects.create_superuser(**superuser)

        self.token_staff = Token.objects.create(user=self.staff)
        self.token_doctor = Token.objects.create(user=self.doctor)
        self.token_manager = Token.objects.create(user=self.manager)
        self.toke_super_user = Token.objects.create(user=self.super_user)

        Owner.objects.bulk_create(
            [
                Owner(**owner_1, created_by=self.manager),
                Owner(**owner_2, created_by=self.manager),
            ]
        )

    def test_doctor_cant_create_a_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_doctor.key)
        response = self.client.post("/api/owners/", owner_1)
        self.assertEquals(response.status_code, 403)

    def test_doctor_cant_update_a_owner(self):
        owner = Owner.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_doctor.key)
        response = self.client.patch(f"/api/owners/{owner.id}/")
        self.assertEquals(response.status_code, 403)

    def test_doctor_cant_delete_a_owner(self):
        owner = Owner.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_doctor.key)
        response = self.client.delete(f"/api/owners/{owner.id}/")
        self.assertEquals(response.status_code, 403)

    def test_staff_cant_delete_a_owner(self):
        owner = Owner.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_staff.key)
        response = self.client.delete(f"/api/owners/{owner.id}/")
        self.assertEquals(response.status_code, 403)

    def test_unauthorized_user_cant_list_owners(self):
        response = self.client.get("/api/owners/")
        self.assertNotEquals(response.status_code, 200)

    def test_staff_can_create_a_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_staff.key)
        response = self.client.post("/api/owners/", owner_3)
        self.assertEquals(response.status_code, 201)

    def test_staff_can_update_a_owner(self):
        owner = Owner.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_staff.key)
        response = self.client.patch(f"/api/owners/{owner.id}/")
        self.assertEquals(response.status_code, 200)
    
    def test_manager_can_create_a_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_manager.key)
        response = self.client.post("/api/owners/", owner_3)
        self.assertEquals(response.status_code, 201)
    
    def test_manager_can_update_a_owner(self):
        owner = Owner.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_manager.key)
        response = self.client.patch(f"/api/owners/{owner.id}/")
        self.assertEquals(response.status_code, 200)

    def test_manager_can_delete_a_owner(self):
        owner = Owner.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_manager.key)
        response = self.client.delete(f"/api/owners/{owner.id}/")
        self.assertEquals(response.status_code, 204)

    def test_only_authenticated_users_can_list_owners(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_doctor.key)
        response = self.client.get("/api/owners/")
        self.assertEquals(response.status_code, 200)

    def test_superuser_can_create_a_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.toke_super_user.key)
        response = self.client.post("/api/owners/", owner_3)
        self.assertEquals(response.status_code, 201)
    
    def test_superuser_can_update_a_owner(self):
        owner = Owner.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.toke_super_user.key)
        response = self.client.patch(f"/api/owners/{owner.id}/")
        self.assertEquals(response.status_code, 200)

    def test_superuser_can_delete_a_owner(self):
        owner = Owner.objects.get(id=1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.toke_super_user.key)
        response = self.client.delete(f"/api/owners/{owner.id}/")
        self.assertEquals(response.status_code, 204)
    