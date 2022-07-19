from pets.models import Pet
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework.views import status
from service_list.models import ServiceList
from services.models import Service
from staffs.models import Staff
from store.models import Store

from .mocks import (
    doctor,
    manager,
    pet_data,
    pet_data_2,
    service_1,
    service_2,
    staff,
    store,
    super_user,
)


class ServiceListVIewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.pet = Pet.objects.create(**pet_data)
        cls.pet_2 = Pet.objects.create(**pet_data_2)

        cls.store = Store.objects.create(**store)

        cls.service_1 = Service.objects.create(**service_1)
        cls.service_2 = Service.objects.create(**service_2)

        cls.admin = Staff.objects.create_superuser(**super_user)
        cls.staff = Staff.objects.create(**staff)
        cls.manager = Staff.objects.create(**manager, store=cls.store)
        cls.doctor = Staff.objects.create(**doctor)

        cls.token_admin = Token.objects.create(user=cls.admin)
        cls.token_staff = Token.objects.create(user=cls.staff)
        cls.token_manager = Token.objects.create(user=cls.manager)
        cls.token_doctor = Token.objects.create(user=cls.doctor)

        cls.sl_data = {
            # "discount": 10,
            "pet_services": [
                {"name": cls.service_1.name},
                {"name": cls.service_2.name},
            ],
        }

        cls.sl_update = {
            "discount": 10,
            "pet_services": [{"name": cls.service_1.name}],
        }

        cls.sl_data_discount_0 = {
            "discount": -5,
            "pet_services": [
                {"name": cls.service_1.name},
                {"name": cls.service_2.name},
            ],
        }

        cls.sl_data_discount_100 = {
            "discount": 101,
            "pet_services": [
                {"name": cls.service_1.name},
                {"name": cls.service_2.name},
            ],
        }

        cls.sl_data_wrong = {
            "pet_services": [
                {"name": cls.service_1.name},
                {"name": cls.service_2.name},
                {"name": "Wrong service"},
            ],
        }

        cls.list_1 = [
            ServiceList.objects.create(
                total=0, pet=cls.pet, delivered_at=cls.store.id
            )
            for _ in range(1, 20)
        ]
        cls.list_2 = [
            ServiceList.objects.create(total=0, pet=cls.pet_2)
            for _ in range(1, 10)
        ]

    def test_servicelist_creation_without_token(self):
        response = self.client.post(
            f"/api/pets/{self.pet.id}/serviceslist/", data=self.sl_data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_sevicelist_creation_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.post(
            f"/api/pets/{self.pet.id}/serviceslist/",
            data=self.sl_data,
            format="json",
        )

        sub_total = self.service_1.price + self.service_2.price

        total_value = sub_total - sub_total * float(response.data["discount"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["pet_id"], self.pet.id)

        self.assertEqual(round(total_value, 2), float(response.data["total"]))

        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)
        self.assertIn("pet_services", response.data)

        for item in response.data["pet_services"]:
            self.assertIn("id", item)
            self.assertIn("name", item)
            self.assertIn("category", item)
            self.assertIn("price", item)

    def test_sevicelist_creation_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.post(
            f"/api/pets/{self.pet.id}/serviceslist/",
            data=self.sl_data,
            format="json",
        )

        sub_total = self.service_1.price + self.service_2.price

        total_value = sub_total - sub_total * float(response.data["discount"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["pet_id"], self.pet.id)

        self.assertEqual(round(total_value, 2), float(response.data["total"]))

        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)
        self.assertIn("pet_services", response.data)

        for item in response.data["pet_services"]:
            self.assertIn("id", item)
            self.assertIn("name", item)
            self.assertIn("category", item)
            self.assertIn("price", item)

    def test_sevicelist_creation_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.post(
            f"/api/pets/{self.pet.id}/serviceslist/",
            data=self.sl_data,
            format="json",
        )

        sub_total = self.service_1.price + self.service_2.price

        total_value = sub_total - sub_total * float(response.data["discount"])

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["pet_id"], self.pet.id)

        self.assertEqual(round(total_value, 2), float(response.data["total"]))

        self.assertIn("id", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)
        self.assertIn("pet_services", response.data)

        for item in response.data["pet_services"]:
            self.assertIn("id", item)
            self.assertIn("name", item)
            self.assertIn("category", item)
            self.assertIn("price", item)

    def test_sevicelist_creation_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.post(
            f"/api/pets/{self.pet.id}/serviceslist/",
            data=self.sl_data,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_services_list_from_pet_without_token(self):
        response = self.client.get(f"/api/pets/{self.pet.id}/serviceslist/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_services_list_from_pet_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.get(f"/api/pets/{self.pet.id}/serviceslist/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.list_1))

        for item in response.data["results"]:
            self.assertEqual(item["pet_id"], self.pet.id)

    def test_list_services_list_from_pet_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.get(f"/api/pets/{self.pet.id}/serviceslist/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.list_1))

        for item in response.data["results"]:
            self.assertEqual(item["pet_id"], self.pet.id)

    def test_list_services_list_from_pet_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.get(f"/api/pets/{self.pet.id}/serviceslist/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.list_1))

        for item in response.data["results"]:
            self.assertEqual(item["pet_id"], self.pet.id)

    def test_list_services_list_from_pet_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.get(f"/api/pets/{self.pet.id}/serviceslist/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.list_1))

        for item in response.data["results"]:
            self.assertEqual(item["pet_id"], self.pet.id)

    def test_list_creation_discount_less_than_0(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.post(
            f"/api/pets/{self.pet.id}/serviceslist/",
            data=self.sl_data_discount_0,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("discount", response.data)
        self.assertEqual(
            "Ensure discount is a number between 0 and 100",
            str(response.data["discount"][0]),
        )

    def test_list_creation_discount_greater_than_100(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.post(
            f"/api/pets/{self.pet.id}/serviceslist/",
            data=self.sl_data_discount_100,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("discount", response.data)
        self.assertEqual(
            "Ensure discount is a number between 0 and 100",
            str(response.data["discount"][0]),
        )

    def test_list_creation_with_wrong_service(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.post(
            f"/api/pets/{self.pet.id}/serviceslist/",
            data=self.sl_data_wrong,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual("service not found", str(response.data["detail"]))

    def test_service_list_update_without_token(self):
        response = self.client.patch(
            f"/api/serviceslist/1/", data=self.sl_update
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_service_list_update_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.patch(
            f"/api/serviceslist/1/", data=self.sl_update, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["pet_id"], self.pet.id)
        self.assertIn("pet_services", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)

    def test_service_list_update_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.patch(
            f"/api/serviceslist/1/", data=self.sl_update, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["pet_id"], self.pet.id)
        self.assertIn("pet_services", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)

    def test_service_list_update_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.patch(
            f"/api/serviceslist/1/", data=self.sl_update, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["pet_id"], self.pet.id)
        self.assertIn("pet_services", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)

    def test_service_list_update_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.patch(
            f"/api/serviceslist/1/", data=self.sl_update, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_service_list_deletion_without_token(self):
        response = self.client.delete(f"/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_service_list_deletion_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.delete(f"/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_service_list_deletion_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.delete(f"/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_service_list_deletion_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.delete(f"/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_service_list_deletion_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.delete(f"/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_service_list_should_exist_after_pet_deletion(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        self.client.delete(
            f"/api/pets/{self.pet.id}/", data=self.sl_update, format="json"
        )

        response = self.client.get("/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn("id", response.data)
        self.assertIn("pet_id", response.data)
        self.assertIn("pet_services", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)

        self.assertEqual(response.data["pet_id"], None)

    def test_service_list_retrieve_without_token(self):
        response = self.client.get(f"/api/pets/{self.pet.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_service_list_retrieve_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.get("/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("pet_id", response.data)
        self.assertIn("pet_services", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)

    def test_service_list_retrieve_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )
        response = self.client.get("/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("pet_id", response.data)
        self.assertIn("pet_services", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)

    def test_service_list_retrieve_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")
        response = self.client.get("/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("pet_id", response.data)
        self.assertIn("pet_services", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)

    def test_service_list_retrieve_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )
        response = self.client.get("/api/serviceslist/1/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)
        self.assertIn("pet_id", response.data)
        self.assertIn("pet_services", response.data)
        self.assertIn("created_at", response.data)
        self.assertIn("discount", response.data)
        self.assertIn("total", response.data)

    def test_service_list_update_with_wrong_values(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.patch(
            "/api/serviceslist/1/",
            data=self.sl_data_wrong,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("detail", response.data)
        self.assertEqual("service not found", str(response.data["detail"]))

    def test_access_financial_reports_without_token(self):

        response = self.client.get(
            f"/api/stores/financial/?store={self.store.id}/"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_financial_reports_superuser(self):

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.get(
            f"/api/stores/financial/?store={self.store.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.list_1))

    def test_access_financial_reports_null_store_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.get(f"/api/stores/financial/?store=null")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.list_2))

    def test_access_financial_reports_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.get(
            f"/api/stores/financial/?store={self.store.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_access_financial_reports_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.get(
            f"/api/stores/financial/?store={self.store.id}"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
