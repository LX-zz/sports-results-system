"""Модели Django для системы спортивных результатов."""

from django.db import models


class Athlete(models.Model):
    full_name = models.CharField(
        max_length=200,
        verbose_name="ФИО спортсмена",
    )

    birth_year = models.PositiveIntegerField(
        verbose_name="Год рождения",
    )

    class Meta:
        ordering = ["full_name"]
        verbose_name = "Спортсмен"
        verbose_name_plural = "Спортсмены"

    def __str__(self):
        return self.full_name


class Discipline(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Название дисциплины",
    )

    unit = models.CharField(
        max_length=30,
        verbose_name="Единица измерения",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name


class Competition(models.Model):
    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
        null=True,
        allow_unicode=True,
        verbose_name="Адрес соревнования",
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Название соревнования",
    )

    date = models.DateField(
        verbose_name="Дата проведения",
    )

    class Meta:
        ordering = ["date", "name"]
        verbose_name = "Соревнование"
        verbose_name_plural = "Соревнования"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse(
            "sports:competition_detail",
            kwargs={"slug": self.slug},
        )

    def save(self, *args, **kwargs):
        from django.utils.text import slugify

        super().save(*args, **kwargs)

        if not self.slug:
            base_slug = slugify(
                self.name,
                allow_unicode=True,
            ) or "competition"

            self.slug = f"{base_slug}-{self.pk}"

            type(self).objects.filter(pk=self.pk).update(
                slug=self.slug
            )


class Result(models.Model):
    athlete = models.ForeignKey(
        Athlete,
        on_delete=models.PROTECT,
        related_name="results",
        verbose_name="Спортсмен",
    )

    discipline = models.ForeignKey(
        Discipline,
        on_delete=models.PROTECT,
        related_name="results",
        verbose_name="Дисциплина",
    )

    competition = models.ForeignKey(
        Competition,
        on_delete=models.PROTECT,
        related_name="results",
        verbose_name="Соревнование",
    )

    result = models.FloatField(
        verbose_name="Спортивный результат",
    )

    place = models.PositiveIntegerField(
        verbose_name="Место",
    )

    standard = models.FloatField(
        verbose_name="Норматив",
    )


    standard_met = models.GeneratedField(
        expression=models.Case(
            models.When(
                result__lte=models.F("standard"),
                then=models.Value(True),
            ),
            default=models.Value(False),
            output_field=models.BooleanField(),
        ),
        output_field=models.BooleanField(),
        db_persist=True,
        verbose_name="Норматив выполнен",
    )

    class Meta:
        ordering = ["place", "id"]
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"

    def __str__(self):
        return (
            f"{self.athlete.full_name}: "
            f"{self.discipline.name} — {self.result}"
        )

    def check_standard(self):
        return self.result <= self.standard

    def get_place_status(self):
        statuses = {
            1: "Золото",
            2: "Серебро",
            3: "Бронза",
        }
        return statuses.get(self.place, "Участник")
