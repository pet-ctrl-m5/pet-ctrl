from django.test import TestCase
from pets.models import Pet
from service_list.models import ServiceList
from services.models import Service

from .mocks import (
    pet_data,
    pet_data_2,
    service_1,
    service_2,
    service_list_1,
    service_list_2,
)


class ServiceListModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.service_1 = Service.objects.create(**service_1)
        cls.service_2 = Service.objects.create(**service_2)

        cls.pet_1 = Pet.objects.create(**pet_data)
        cls.pet_2 = Pet.objects.create(**pet_data_2)

        cls.service_list_1 = ServiceList(**service_list_1)
        cls.service_list_2 = ServiceList(**service_list_2)

    def test_service_list_creation_with_pet(self):
        self.service_list_1.pet = self.pet_1

        total = round(service_1["price"] + service_2["price"], 2)

        disc = (total * self.service_list_1.discount) / 100

        self.service_list_1.total = round((total - disc), 2)

        self.service_list_1.save()

        self.service_list_1.pet_services.set([self.service_1, self.service_2])
        self.service_list_1.save()

        new_service_list = ServiceList.objects.get(pk=self.service_list_1.id)

        self.assertEqual(self.service_list_1.id, new_service_list.id)
        self.assertEqual(self.service_list_1.pet, new_service_list.pet)
        self.assertEqual(
            self.service_list_1.discount, new_service_list.discount
        )
        self.assertEqual(
            self.service_list_1.total, float(new_service_list.total)
        )
        self.assertEqual(
            self.service_list_1.pet_services, new_service_list.pet_services
        )

    def test_service_list_is_nullable(self):

        total = round(service_1["price"] + service_2["price"], 2)

        disc = (total * self.service_list_1.discount) / 100

        self.service_list_1.total = round((total - disc), 2)

        self.service_list_1.save()

        self.service_list_1.pet_services.set([self.service_1, self.service_2])
        self.service_list_1.save()

        new_service_list = ServiceList.objects.get(pk=self.service_list_1.id)

        self.assertEqual(self.service_list_1.id, new_service_list.id)
        self.assertEqual(self.service_list_1.pet, new_service_list.pet)
        self.assertEqual(
            self.service_list_1.discount, new_service_list.discount
        )
        self.assertEqual(
            self.service_list_1.total, float(new_service_list.total)
        )
        self.assertEqual(
            self.service_list_1.pet_services, new_service_list.pet_services
        )

    # def test_many_services_list_can_have_repeated_services(self):
    #     # self.service_list_1.pet = self.pet_1

    #     total = round(service_1["price"] + service_2["price"], 2)

    #     disc = (total * self.service_list_1.discount) / 100

    #     lists = [
    #         ServiceList.objects.create(
    #             **service_list_1, total=round(total - disc, 2)
    #         )
    #         for _ in range(1, 20)
    #     ]

    #     for item in lists:
    #         item.pet_services.set([self.service_1, self.service_2])

    #     self.assertEqual(len(lists), )
