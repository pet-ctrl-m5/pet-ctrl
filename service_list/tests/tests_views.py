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
    service_1,
    service_2,
    staff,
    super_user,
)


class ServiceListVIewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.pet = Pet.objects.create(**pet_data)
        cls.pet_2 = Pet.objects.create(**pet_data_2)

        cls.admin = Staff.objects.create_superuser(**super_user)
        cls.staff = Staff.objects.create(**staff)
        cls.manager = Staff.objects.create(**manager)
        cls.doctor = Staff.objects.create(**doctor)

        cls.token_admin = Token.objects.create(user=cls.admin)
        cls.token_staff = Token.objects.create(user=cls.staff)
        cls.token_manager = Token.objects.create(user=cls.manager)
        cls.token_doctor = Token.objects.create(user=cls.doctor)

    def test_servicelist_creation_without_token(self):
        ...
