from typing import List, Optional

from models import Competition


def add_competition(
    competitions: List[Competition],
    name: str,
    competition_date: str,
) -> Competition:
    """Создать и добавить соревнование."""
    for competition in competitions:
        same_name = competition.name.lower() == name.strip().lower()
        same_date = competition.date == competition_date.strip()

        if same_name and same_date:
            raise ValueError("Такое соревнование уже существует")

    competition_id = (
        max(
            (competition.id for competition in competitions),
            default=0,
        )
        + 1
    )

    competition = Competition(
        competition_id=competition_id,
        name=name,
        competition_date=competition_date,
    )

    competitions.append(competition)
    return competition


def find_competitions(
    competitions: List[Competition],
    query: str,
) -> List[Competition]:
    """Найти соревнования по названию."""
    query = query.lower().strip()

    return [
        competition
        for competition in competitions
        if query in competition.name.lower()
    ]


def sort_competitions(
    competitions: List[Competition],
) -> List[Competition]:
    """Отсортировать соревнования по дате."""
    return sorted(
        competitions,
        key=lambda competition: competition.date,
    )


def get_competition_by_id(
    competitions: List[Competition],
    competition_id: int,
) -> Optional[Competition]:
    """Найти соревнование по ID."""
    for competition in competitions:
        if competition.id == competition_id:
            return competition

    return None
