"""Автоматические тесты Django ORM для ПР9."""

from django.db.models import Avg, Count, F
from django.test import TestCase
from django.urls import reverse

from .models import Athlete, Competition, Discipline, Result


class SportsORMTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.athlete = Athlete.objects.create(
            full_name="Тестовый Спортсмен",
            birth_year=2006,
        )

        cls.discipline = Discipline.objects.create(
            name="Бег 100 метров",
            unit="сек.",
        )

        cls.competition = Competition.objects.create(
            name="Тестовый чемпионат",
            date="2026-10-10",
        )

        for index in range(7):
            Result.objects.create(
                athlete=cls.athlete,
                discipline=cls.discipline,
                competition=cls.competition,
                result=11.0 + index * 0.1,
                place=index + 1,
                standard=12.0,
            )

    def test_create_and_read(self):
        athlete = Athlete.objects.get(
            pk=self.athlete.pk
        )
        self.assertEqual(
            athlete.full_name,
            "Тестовый Спортсмен",
        )

    def test_filter_and_exclude(self):
        self.assertEqual(
            Athlete.objects.filter(
                birth_year__gte=2006
            ).count(),
            1,
        )

        self.assertEqual(
            Result.objects.exclude(
                place=1
            ).count(),
            6,
        )

    def test_related_objects(self):
        result = Result.objects.select_related(
            "athlete",
            "discipline",
            "competition",
        ).first()

        self.assertEqual(
            result.athlete.full_name,
            "Тестовый Спортсмен",
        )

        self.assertEqual(
            result.discipline.name,
            "Бег 100 метров",
        )

    def test_aggregation(self):
        statistics = Result.objects.aggregate(
            count=Count("id"),
            average=Avg("result"),
        )

        self.assertEqual(statistics["count"], 7)
        self.assertIsNotNone(statistics["average"])

    def test_filter_by_related_field(self):
        results = Result.objects.filter(
            athlete__full_name__icontains="Тестовый"
        )

        self.assertEqual(results.count(), 7)

    def test_standard_filter(self):
        results = Result.objects.filter(
            result__lte=F("standard")
        )

        self.assertEqual(results.count(), 7)

    def test_results_pagination(self):
        response = self.client.get(
            reverse("sports:results")
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["results"]),
            5,
        )

        response = self.client.get(
            reverse("sports:results"),
            {"page": "2"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.context["results"]),
            2,
        )

    def test_search_page(self):
        response = self.client.get(
            reverse("sports:athlete_search"),
            {"name": "Тестовый"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Тестовый Спортсмен",
        )

    def test_results_filter(self):
        response = self.client.get(
            reverse("sports:results"),
            {"place": "1"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["total_count"],
            1,
        )

    def test_missing_result(self):
        response = self.client.get(
            reverse(
                "sports:result_detail",
                args=[99999],
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_update_and_delete(self):
        athlete = Athlete.objects.create(
            full_name="Временный Спортсмен",
            birth_year=2005,
        )

        athlete.birth_year = 2004
        athlete.save()

        self.assertEqual(
            Athlete.objects.get(pk=athlete.pk).birth_year,
            2004,
        )

        athlete.delete()

        self.assertFalse(
            Athlete.objects.filter(
                full_name="Временный Спортсмен"
            ).exists()
        )
