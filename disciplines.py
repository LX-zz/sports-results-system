"""Функции для работы со спортивными дисциплинами."""

from typing import Optional


def add_discipline(
    disciplines: list[dict],
    name: str,
    unit: str,
) -> dict:
    """Добавить спортивную дисциплину."""
    name = name.strip()
    unit = unit.strip()

    if not name:
        raise ValueError("Название дисциплины не может быть пустым")

    if not unit:
        raise ValueError("Единица измерения не может быть пустой")

    for discipline in disciplines:
        if discipline["name"].lower() == name.lower():
            raise ValueError("Такая дисциплина уже существует")

    new_discipline = {
        "id": max(
            (item["id"] for item in disciplines),
            default=0,
        ) + 1,
        "name": name,
        "unit": unit,
    }

    disciplines.append(new_discipline)
    return new_discipline


def find_disciplines(
    disciplines: list[dict],
    query: str,
) -> list[dict]:
    """Найти дисциплины по названию."""
    query = query.lower().strip()

    return [
        discipline
        for discipline in disciplines
        if query in discipline["name"].lower()
    ]


def sort_disciplines(
    disciplines: list[dict],
) -> list[dict]:
    """Отсортировать дисциплины по названию."""
    return sorted(
        disciplines,
        key=lambda item: item["name"].lower(),
    )


def get_discipline_by_id(
    disciplines: list[dict],
    discipline_id: int,
) -> Optional[dict]:
    """Найти дисциплину по ID."""
    for discipline in disciplines:
        if discipline["id"] == discipline_id:
            return discipline

    return None
