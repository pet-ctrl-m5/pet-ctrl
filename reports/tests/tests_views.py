from owners.models import Owner
from pets.models import Pet
from reports.models import Report
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from staffs.models import Staff

from .mocks import (
    doctor,
    manager,
    pet_data,
    pet_data_2,
    pet_owner,
    pet_owner_2,
    report_data,
    report_data_2,
    staff,
    super_user,
)

# /api/reports/pets/id_pet/ (POST, GET)
# /api/reports/id_report (GET, PATCH, DELETE)
# /api/reports/ (GET)


class TestReportViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:

        cls.owner = Owner.objects.create(**pet_owner)

        cls.pet = Pet.objects.create(**pet_data, owner=cls.owner)
        cls.pet_2 = Pet.objects.create(**pet_data_2)

        cls.admin = Staff.objects.create_superuser(**super_user)
        cls.staff = Staff.objects.create(**staff)
        cls.manager = Staff.objects.create(**manager)
        cls.doctor = Staff.objects.create(**doctor)

        cls.token_admin = Token.objects.create(user=cls.admin)
        cls.token_staff = Token.objects.create(user=cls.staff)
        cls.token_manager = Token.objects.create(user=cls.manager)
        cls.token_doctor = Token.objects.create(user=cls.doctor)

        cls.reports_pet_1 = [
            Report.objects.create(**report_data, pet=cls.pet)
            for _ in range(0, 20)
        ]

        cls.reports_pet_2 = [
            Report.objects.create(**report_data, pet=cls.pet_2)
            for _ in range(0, 10)
        ]

    def test_report_creation_without_token(self):
        pet_id = self.pet.id

        response = self.client.post(
            f"/api/reports/pets/{pet_id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_report_creation_superuser_success(self):
        pet_id = self.pet.id

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.post(
            f"/api/reports/pets/{pet_id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(report_data, response.data)
        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_report_creation_manager_success(self):
        pet_id = self.pet.id

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.post(
            f"/api/reports/pets/{pet_id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(report_data, response.data)
        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_report_creation_staff_failure(self):
        pet_id = self.pet.id

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.post(
            f"/api/reports/pets/{pet_id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_report_creation_doctor_success(self):
        pet_id = self.pet.id

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.post(
            f"/api/reports/pets/{pet_id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertDictContainsSubset(report_data, response.data)
        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_list_reports_from_pet_without_token(self):
        response = self.client.get(
            f"/api/reports/pets/{self.pet.id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_reports_from_pet_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.get(
            f"/api/reports/pets/{self.pet.id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], self.pet.reports.count())

    def test_list_reports_from_pet_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.get(
            f"/api/reports/pets/{self.pet.id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], self.pet.reports.count())

    def test_list_reports_from_pet_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.get(
            f"/api/reports/pets/{self.pet.id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], self.pet.reports.count())

    def test_list_reports_from_pet_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.get(
            f"/api/reports/pets/{self.pet.id}/", data=report_data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["count"], self.pet.reports.count())

    def test_update_report_without_token(self):
        response = self.client.patch("/api/reports/1/", data=report_data_2)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_reports_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.patch("/api/reports/1/", data=report_data_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(report_data_2, response.data)

        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_update_reports_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.patch("/api/reports/1/", data=report_data_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(report_data_2, response.data)

        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_update_reports_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.patch("/api/reports/1/", data=report_data_2)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_reports_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.patch("/api/reports/1/", data=report_data_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(report_data_2, response.data)

        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_delete_report_without_token(self):
        response = self.client.delete("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_report_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.delete("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_report_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )
        response = self.client.delete("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_report_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")
        response = self.client.delete("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_report_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )
        response = self.client.delete("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_reports_persists_after_pet_deletion(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        self.client.delete(f"/api/pets/{self.pet.id}/")

        response = self.client.get("/api/reports/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        all_reports = Report.objects.all()

        self.assertEqual(response.data["count"], all_reports.count())

        for report in response.data["results"]:

            self.assertEqual(report["pet_info"], None)

    def test_report_retrieve_without_token(self):
        response = self.client.get("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_report_retrieve_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.get("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(report_data, response.data)
        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_report_retrieve_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.get("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(report_data, response.data)
        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_report_retrieve_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.get("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(report_data, response.data)
        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_report_retrieve_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.get("/api/reports/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(report_data, response.data)
        self.assertIn("pet_info", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("updated_at", response.data)
        self.assertEqual(
            response.data["pet_info"],
            {
                "id": self.pet.id,
                "name": self.pet.name,
                "owner": self.pet.owner.name,
            },
        )

    def test_report_should_show_pet_info_pet_without_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.get(f"/api/reports/{self.reports_pet_2[0].id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["pet_info"]["owner"], None)
