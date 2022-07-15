from owners.models import Owner
from pets.models import Pet
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
    staff,
    super_user,
)

# ROTAS
# - api/pets/owner/<int:owner_id>/ (POST, GET)
# - api/pets/ (GET)
# - api/pets/<int:pet_id>/ (GET, PATCH, DELETE)


class TestPetsViews(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner = Owner.objects.create(**pet_owner)
        cls.owner_2 = Owner.objects.create(**pet_owner_2)

        cls.admin = Staff.objects.create_superuser(**super_user)
        cls.staff = Staff.objects.create(**staff)
        cls.manager = Staff.objects.create(**manager)
        cls.doctor = Staff.objects.create(**doctor)

        cls.token_admin = Token.objects.create(user=cls.admin)
        cls.token_staff = Token.objects.create(user=cls.staff)
        cls.token_manager = Token.objects.create(user=cls.manager)
        cls.token_doctor = Token.objects.create(user=cls.doctor)

        cls.pets_owner_1 = [
            Pet.objects.create(**pet_data, owner=cls.owner)
            for _ in range(1, 20)
        ]

    def test_pet_creation_without_token(self):
        owner_id = self.owner.id
        response = self.client.post(
            f"/api/pets/owner/{owner_id}/", data=pet_data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pet_creation_superuser_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.post(
            f"/api/pets/owner/{self.owner.id}/", data=pet_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertDictContainsSubset(pet_data, response.data)

        self.assertIn("owner_id", response.data)
        self.assertIn("reports", response.data)
        self.assertIn("customer_services", response.data)

    def test_pet_creation_manager_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.post(
            f"/api/pets/owner/{self.owner.id}/", data=pet_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertDictContainsSubset(pet_data, response.data)

        self.assertIn("owner_id", response.data)
        self.assertIn("reports", response.data)
        self.assertIn("customer_services", response.data)

    def test_pet_creation_staff_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.post(
            f"/api/pets/owner/{self.owner.id}/", data=pet_data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertDictContainsSubset(pet_data, response.data)

        self.assertIn("owner_id", response.data)
        self.assertIn("reports", response.data)
        self.assertIn("customer_services", response.data)

    def test_pet_creation_doctor_failure(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.post(
            f"/api/pets/owner/{self.owner.id}/", data=pet_data
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pet_creation_without_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.post(
            f"/api/pets/owner/{self.owner.id}/", data={}
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", response.data)
        self.assertIn("type", response.data)
        self.assertIn("breed", response.data)
        self.assertIn("birthday", response.data)

    def test_pet_listing_by_owner_without_token(self):
        response = self.client.get(f"/api/pets/owner/{self.owner.id}/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pet_listing_by_owner_superuser(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.get(f"/api/pets/owner/{self.owner.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.pets_owner_1))

    def test_pet_listing_by_owner_manager(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )
        response = self.client.get(f"/api/pets/owner/{self.owner.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.pets_owner_1))

    def test_pet_listing_by_owner_staff(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")
        response = self.client.get(f"/api/pets/owner/{self.owner.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.pets_owner_1))

    def test_pet_listing_by_owner_doctor(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )
        response = self.client.get(f"/api/pets/owner/{self.owner.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.pets_owner_1))

    def test_pet_update_without_token(self):
        response = self.client.patch(f"/api/pets/1/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pet_update_superuser_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.patch(f"/api/pets/1/", data=pet_data_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(pet_data_2, response.data)

    def test_pet_update_manager_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.patch(f"/api/pets/1/", data=pet_data_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(pet_data_2, response.data)

    def test_pet_update_staff_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.patch(f"/api/pets/1/", data=pet_data_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(pet_data_2, response.data)

    def test_pet_update_doctor_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.patch(f"/api/pets/1/", data=pet_data_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertDictContainsSubset(pet_data_2, response.data)

    def test_pet_delete_without_token(self):
        response = self.client.delete(f"/api/pets/1/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pet_delete_superuser_success(self):

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")

        response = self.client.delete(f"/api/pets/1/")

        pets = Pet.objects.all()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(None, response.data)
        self.assertEqual(len(self.pets_owner_1) - 1, len(pets))

    def test_pet_delete_manager_success(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )

        response = self.client.delete(f"/api/pets/1/")

        pets = Pet.objects.all()
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(None, response.data)
        self.assertEqual(len(self.pets_owner_1) - 1, len(pets))

    def test_pet_delete_staff_failure(self):

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")

        response = self.client.delete(f"/api/pets/1/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pet_delete_doctor_failure(self):

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )

        response = self.client.delete(f"/api/pets/1/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_pet_list_without_token(self):
        response = self.client.get(f"/api/pets/")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pet_list_superuser_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.get(f"/api/pets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.pets_owner_1))

    def test_pet_list_manager_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )
        response = self.client.get(f"/api/pets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.pets_owner_1))

    def test_pet_list_staff_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")
        response = self.client.get(f"/api/pets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.pets_owner_1))

    def test_pet_list_doctor_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )
        response = self.client.get(f"/api/pets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], len(self.pets_owner_1))

    def test_pet_retrieve_without_token(self):
        response = self.client.get(f"/api/pets/1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_pet_retrieve_superuser_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_admin}")
        response = self.client.get(f"/api/pets/1/")

        pet_1 = Pet.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], pet_1.id)
        self.assertEqual(response.data["name"], pet_1.name)
        self.assertEqual(response.data["type"], pet_1.type)
        self.assertEqual(response.data["breed"], pet_1.breed)
        self.assertEqual(response.data["birthday"], str(pet_1.birthday))
        self.assertEqual(response.data["reports"], [])
        self.assertEqual(response.data["customer_services"], [])

    def test_pet_retrieve_manager_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_manager}"
        )
        response = self.client.get(f"/api/pets/1/")

        pet_1 = Pet.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], pet_1.id)
        self.assertEqual(response.data["name"], pet_1.name)
        self.assertEqual(response.data["type"], pet_1.type)
        self.assertEqual(response.data["breed"], pet_1.breed)
        self.assertEqual(response.data["birthday"], str(pet_1.birthday))
        self.assertEqual(response.data["reports"], [])
        self.assertEqual(response.data["customer_services"], [])

    def test_pet_retrieve_staff_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token_staff}")
        response = self.client.get(f"/api/pets/1/")

        pet_1 = Pet.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], pet_1.id)
        self.assertEqual(response.data["name"], pet_1.name)
        self.assertEqual(response.data["type"], pet_1.type)
        self.assertEqual(response.data["breed"], pet_1.breed)
        self.assertEqual(response.data["birthday"], str(pet_1.birthday))
        self.assertEqual(response.data["reports"], [])
        self.assertEqual(response.data["customer_services"], [])

    def test_pet_retrieve_doctor_success(self):
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )
        response = self.client.get(f"/api/pets/1/")

        pet_1 = Pet.objects.get(pk=1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], pet_1.id)
        self.assertEqual(response.data["name"], pet_1.name)
        self.assertEqual(response.data["type"], pet_1.type)
        self.assertEqual(response.data["breed"], pet_1.breed)
        self.assertEqual(response.data["birthday"], str(pet_1.birthday))
        self.assertEqual(response.data["reports"], [])
        self.assertEqual(response.data["customer_services"], [])

    def test_pet_owner_info_no_owner(self):
        no_owner_pet = Pet.objects.create(**pet_data)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token_doctor}"
        )
        response = self.client.get(f"/api/pets/{no_owner_pet.id}/")

        pet = Pet.objects.get(pk=no_owner_pet.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], pet.id)
        self.assertEqual(response.data["name"], pet.name)
        self.assertEqual(response.data["type"], pet.type)
        self.assertEqual(response.data["breed"], pet.breed)
        self.assertEqual(response.data["birthday"], str(pet.birthday))
        self.assertEqual(response.data["reports"], [])
        self.assertEqual(response.data["customer_services"], [])
        self.assertEqual(response.data["owner_info"], None)
