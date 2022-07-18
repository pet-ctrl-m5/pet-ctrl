from django.test import TestCase
from service_list.models import ServiceList
from services.models import Service

from .mocks import admin, doctor, manager, service_1, service_2, staff


class ServiceModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.service_1 = Service(**service_1)
        cls.service_2 = Service.objects.create(**service_2)

        cls.service_list = {
            "discount": 10,
        }
        cls.service_list_2 = {}

        cls.list = [
            ServiceList.objects.create(**cls.service_list, total=0)
            for _ in range(1, 20)
        ]

        cls.list_2 = [
            ServiceList.objects.create(**cls.service_list_2, total=0)
            for _ in range(1, 20)
        ]

        return super().setUpTestData()

    def test_service_creation(self):
        self.service_1.save()

        service = Service.objects.get(pk=2)

        self.assertEqual(service.id, self.service_1.id)
        self.assertEqual(service.name, self.service_1.name)
        self.assertEqual(service.category, self.service_1.category)
        self.assertEqual(float(service.price), self.service_1.price)
        self.assertEqual(service.is_active, self.service_1.is_active)
        self.assertEqual(service.created_at, self.service_1.created_at)
        self.assertEqual(service.updated_at, self.service_1.updated_at)

    def test_service_relation(self):
        for item in self.list:
            item.pet_services.add(self.service_2)
            item.save()

        for item in self.list:
            self.assertIn(self.service_2, item.pet_services.all())

    def test_services_can_be_in_different_services_list(self):

        for item in self.list:
            item.pet_services.add(self.service_2)

        for item in self.list_2:
            item.pet_services.add(self.service_2)

        for item in self.list:
            self.assertIn(self.service_2, item.pet_services.all())

        for item in self.list_2:
            self.assertIn(self.service_2, item.pet_services.all())
