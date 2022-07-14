from django.test import TestCase
from ..models import Owner
from staffs.models import Staff
from django.db import IntegrityError
from .mock import staff_manager, owner_1


class OwnerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.staff = Staff.objects.create(**staff_manager)

        cls.owner = Owner.objects.create(
            **owner_1,
            created_by=Staff.objects.get(id=1),
        )

    def test_owner_name_max_length(self):
        max_length = self.owner._meta.get_field("name").max_length
        self.assertEquals(max_length, 255)

    def test_owner_phone_number_max_length(self):
        max_length = self.owner._meta.get_field("phone_number").max_length
        self.assertEquals(max_length, 20)

    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            Owner.objects.create(
                **owner_1,
                created_by=Staff.objects.get(id=1),
            )

    def test_owner_has_information_fields(self):
        self.assertEquals(self.owner.name, owner_1["name"])
        self.assertEquals(self.owner.email, owner_1["email"])
        self.assertEquals(self.owner.address, owner_1["address"])
        self.assertEquals(self.owner.phone_number, owner_1["phone_number"])

    def test_create_owner_without_staff_id(self):
        with self.assertRaises(IntegrityError):
            Owner.objects.create(
                **owner_1,
            )
