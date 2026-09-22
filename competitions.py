"""Функции для работы с соревнованиями."""

from typing import Optional


def add_competition(
    competitions: list[dict],
    name: str,
    competition_date: str,
) -> dict:
    """Добавить соревнование."""
    name = name.strip()

    if not name:
        raise ValueError("Название соревнования не может быть пустым")

    for competition in competitions:
        same_name = competition["name"].lower() == name.lower()
        same_date = competition["date"] == competition_date

        if same_name and same_date:
            raise ValueError("Такое соревнование уже существует")

    new_competition = {
        "id": max(
            (item["id"] for item in competitions),
            default=0,
        ) + 1,
        "name": name,
        "date": competition_date,
    }

    competitions.append(new_competition)
    return new_competition


def find_competitions(
    competitions: list[dict],
    query: str,
) -> list[dict]:
    """Найти соревнования по названию."""
    query = query.lower().strip()

    return [
        competition
        for competition in competitions
        if query in competition["name"].lower()
    ]


def sort_competitions(
    competitions: list[dict],
) -> list[dict]:
    """Отсортировать соревнования по дате."""
    return sorted(
        competitions,
        key=lambda item: item["date"],
    )


def get_competition_by_id(
    competitions: list[dict],
    competition_id: int,
) -> Optional[dict]:
    """Найти соревнование по ID."""
    for competition in competitions:
        if competition["id"] == competition_id:
            return competition

    return None
