from django.test import TestCase
from pets.models import Pet
from reports.models import Report

from .mocks import pet_data, pet_data_2, report_data


class ReportModelTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.pet = Pet.objects.create(**pet_data)
        cls.report = Report(**report_data)
        cls.reports_list = [Report(**report_data) for _ in range(15)]

    def test_report_creation_with_pet(self):
        self.report.pet = self.pet
        self.report.save()

        new_report = Report.objects.get(pk=self.report.id)

        self.assertEqual(self.report.id, new_report.id)
        self.assertEqual(self.report.report, new_report.report)
        self.assertEqual(self.report.created_at, new_report.created_at)
        self.assertEqual(self.report.updated_at, new_report.updated_at)
        self.assertEqual(self.report.pet_id, new_report.pet_id)

    def test_pets_can_have_multiple_reports(self):
        for report in self.reports_list:
            report.pet = self.pet
            report.save()

        self.assertEqual(len(self.reports_list), self.pet.reports.count())

    def test_report_can_have_only_one_pet(self):
        pet_2 = Pet.objects.create(**pet_data_2)

        for report in self.reports_list:
            report.pet = self.pet
            report.save()

        for report in self.reports_list:
            report.pet = pet_2
            report.save()

        for report in self.reports_list:
            self.assertIn(report, pet_2.reports.all())
            self.assertNotIn(report, self.pet.reports.all())
