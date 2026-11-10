"""Перенос данных из SQLite ПР7 в Django ORM."""

import os
import sqlite3
import sys
from datetime import date
from pathlib import Path

import django


BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "sports_results.sqlite"

sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "sports_site.settings",
)

django.setup()


def read_source_data():
    """Прочитать исходную базу без внесения изменений."""
    if not SOURCE_DB.is_file():
        raise FileNotFoundError(
            f"Исходная база не найдена: {SOURCE_DB}"
        )

    conn = sqlite3.connect(
        SOURCE_DB.as_uri() + "?mode=ro",
        uri=True,
    )

    try:
        conn.row_factory = sqlite3.Row

        tables = (
            "athletes",
            "disciplines",
            "competitions",
            "results",
        )

        data = {}

        for table in tables:
            rows = conn.execute(
                f"SELECT * FROM {table} ORDER BY id"
            ).fetchall()

            data[table] = [
                dict(row) for row in rows
            ]

        return data

    finally:
        conn.close()


def main():
    from django.db import transaction

    from sports.models import (
        Athlete,
        Competition,
        Discipline,
        Result,
    )

    data = read_source_data()

    print("Исходная база ПР7:")
    for table, rows in data.items():
        print(f"  {table}: {len(rows)}")

    with transaction.atomic():

        # 1. Спортсмены
        for row in data["athletes"]:
            Athlete.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "full_name": row["full_name"],
                    "birth_year": row["birth_year"],
                },
            )

        # 2. Дисциплины
        for row in data["disciplines"]:
            Discipline.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "unit": row["unit"],
                },
            )

        # 3. Соревнования
        for row in data["competitions"]:
            Competition.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "name": row["name"],
                    "date": date.fromisoformat(row["date"]),
                },
            )

        # 4. Спортивные результаты
        for row in data["results"]:
            Result.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "athlete_id": row["athlete_id"],
                    "discipline_id": row["discipline_id"],
                    "competition_id": row["competition_id"],
                    "result": row["result"],
                    "place": row["place"],
                    "standard": row["standard"],
                },
            )

    print()
    print("Данные успешно перенесены в Django ORM.")
    print()
    print("Количество записей в Django:")

    print("Спортсмены:", Athlete.objects.count())
    print("Дисциплины:", Discipline.objects.count())
    print("Соревнования:", Competition.objects.count())
    print("Результаты:", Result.objects.count())


if __name__ == "__main__":
    main()
