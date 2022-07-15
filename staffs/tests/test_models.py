import ipdb
from django.db import IntegrityError
from django.test import TestCase
from store.models import Store

from ..models import Staff
from .mock import doctor, manager, staff, store, superuser


class StaffModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.store = Store.objects.create(**store)
        cls.superuser = Staff.objects.create_superuser(**superuser)
        cls.doctor = Staff.objects.create_user(**doctor, store=cls.store)
        cls.manager = Staff.objects.create_user(**manager, store=cls.store)
        cls.staff = Staff.objects.create_user(**staff, store=cls.store)

    def test_staff_max_length_attributes(self):
        max_length_username = self.staff._meta.get_field("username").max_length
        max_length_first_name = self.staff._meta.get_field("first_name").max_length
        max_length_last_name = self.staff._meta.get_field("last_name").max_length
        self.assertEqual(max_length_username, 100)
        self.assertEqual(max_length_first_name, 50)
        self.assertEqual(max_length_last_name, 50)

    def test_staff_same_name(self):
        with self.assertRaises(IntegrityError):
            Staff.objects.create_user(**staff, store=self.store)

    def test_staff_has_information_fields(self):
        self.assertEqual(self.staff.username, staff["username"])
        self.assertEqual(self.staff.first_name, staff["first_name"])
        self.assertEqual(self.staff.last_name, staff["last_name"])
        self.assertEqual(self.staff.is_manager, staff["is_manager"])
        self.assertEqual(self.staff.is_doctor, staff["is_doctor"])
        self.assertEqual(self.staff.is_staff, staff["is_staff"])

    def test_staff_is_active_default_true(self):
        default_staff = self.staff._meta.get_field("is_active").default
        default_doctor = self.doctor._meta.get_field("is_active").default
        default_manager = self.manager._meta.get_field("is_active").default
        default_superuser = self.superuser._meta.get_field("is_active").default
        self.assertTrue(default_staff)
        self.assertTrue(default_doctor)
        self.assertTrue(default_manager)
        self.assertTrue(default_superuser)

    def test_staff_attach_store_correctly(self):
        self.assertEqual(self.staff.store, self.store)
