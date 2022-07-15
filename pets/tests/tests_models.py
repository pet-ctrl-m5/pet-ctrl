from django.db import IntegrityError
from django.test import TestCase
from owners.models import Owner
from pets.models import Pet
from staffs.models import Staff

from .mocks import pet_data, pet_owner, pet_owner_2, staff


class PetModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.staff = Staff.objects.create(**staff)
        cls.owner = Owner.objects.create(**pet_owner, created_by=cls.staff)
        cls.pet = Pet(**pet_data)
        cls.pets_list = [Pet(**pet_data) for _ in range(15)]

    def test_pet_creation_success(self):
        self.pet.owner = self.owner
        self.pet.save()

        new_pet = Pet.objects.get(pk=self.pet.id)

        self.assertEqual(self.pet.id, new_pet.id)
        self.assertEqual(self.pet.name, new_pet.name)
        self.assertEqual(self.pet.type, new_pet.type)
        self.assertEqual(self.pet.breed, new_pet.breed)
        self.assertEqual(self.pet.birthday, str(new_pet.birthday))
        self.assertEqual(self.pet.is_alive, new_pet.is_alive)
        self.assertEqual(self.pet.owner.id, new_pet.owner_id)
        self.assertIsInstance(self.pet.owner, Owner)

    def test_pet_creation_without_owner(self):

        self.pet.save()

        new_pet = Pet.objects.get(pk=self.pet.id)

        self.assertEqual(self.pet.id, new_pet.id)
        self.assertEqual(self.pet.name, new_pet.name)
        self.assertEqual(self.pet.type, new_pet.type)
        self.assertEqual(self.pet.breed, new_pet.breed)
        self.assertEqual(self.pet.birthday, str(new_pet.birthday))
        self.assertEqual(self.pet.is_alive, new_pet.is_alive)
        self.assertEqual(None, new_pet.owner_id)

    def test_owner_can_have_multiples_pets(self):
        for pet in self.pets_list:
            pet.owner = self.owner
            pet.save()

        self.assertEquals(len(self.pets_list), self.owner.pets.count())

    def test_pet_belong_to_one_owner(self):
        owner_2 = Owner.objects.create(**pet_owner_2, created_by=self.staff)

        for pet in self.pets_list:
            pet.owner = self.owner
            pet.save()

        for pet in self.pets_list:
            pet.owner = owner_2
            pet.save()

        for pet in self.pets_list:
            self.assertIn(pet, owner_2.pets.all())
            self.assertNotIn(pet, self.owner.pets.all())
