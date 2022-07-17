from django.test import TestCase
from .mock import store_1, store_2, store_3
from ..models import Store
from django.db import IntegrityError


class StoreModelTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.store = Store.objects.create(**store_1)
        cls.store_tst_2 = Store.objects.create(**store_2)
        cls.store_tst_3 = Store.objects.create(**store_3)

    def test_store_max_length_attributes(self):
        max_length_name = self.store._meta.get_field("name").max_length
        max_length_address = self.store._meta.get_field("address").max_length
        max_length_state = self.store._meta.get_field("state").max_length
        max_length_city = self.store._meta.get_field("city").max_length
        self.assertEqual(max_length_name, 255)
        self.assertEqual(max_length_address, 255)
        self.assertEqual(max_length_state, 20)
        self.assertEqual(max_length_city, 50)

    def test_if_name_is_unique(self):
        with self.assertRaises(IntegrityError):
            Store.objects.create(**store_1)

    def test_store_has_information_fields(self):
        self.assertEquals(self.store.name, store_1["name"])
        self.assertEquals(self.store.address, store_1["address"])
        self.assertEquals(self.store.state, store_1["state"])
        self.assertEquals(self.store.city, store_1["city"])
        self.assertEquals(self.store.is_active, store_1["is_active"])

    def test_is_active_default(self):
        default = self.store_tst_3._meta.get_field("is_active").default
        self.assertTrue(default)

    def test_state_is_choice(self):
        choices = self.store_tst_2._meta.get_field("state").choices
        self.assertIn((self.store.state, self.store.get_state_display()), choices)
