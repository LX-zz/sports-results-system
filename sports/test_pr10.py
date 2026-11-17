from django.test import TestCase
from django.urls import reverse

from sports.models import Athlete, Competition, Discipline, Result


class PR10Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.athlete = Athlete.objects.create(
            full_name="Иван Иванов",
            birth_year=2004,
        )
        cls.discipline = Discipline.objects.create(
            name="Бег 100 м",
            unit="с",
        )
        cls.competition = Competition.objects.create(
            name="Тестовый чемпионат",
            date="2026-11-17",
        )
        cls.result = Result.objects.create(
            athlete=cls.athlete,
            discipline=cls.discipline,
            competition=cls.competition,
            result=11.5,
            place=1,
            standard=12.0,
        )

    def test_competition_slug(self):
        self.assertTrue(self.competition.slug)
        self.assertIn(
            str(self.competition.pk),
            self.competition.slug,
        )

    def test_competition_detail(self):
        response = self.client.get(
            self.competition.get_absolute_url()
        )
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_competition(self):
        response = self.client.get(
            reverse(
                "sports:competition_detail",
                kwargs={"slug": "missing-999"},
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_generated_standard(self):
        self.result.refresh_from_db()
        self.assertTrue(self.result.standard_met)

        self.result.result = 12.5
        self.result.save()
        self.result.refresh_from_db()

        self.assertFalse(self.result.standard_met)

    def test_related_objects(self):
        result = Result.objects.select_related(
            "athlete",
            "discipline",
            "competition",
        ).get(pk=self.result.pk)

        self.assertEqual(
            result.athlete.full_name,
            "Иван Иванов",
        )
