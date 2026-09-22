from typing import List, Optional

from models import Discipline


def add_discipline(
    disciplines: List[Discipline],
    name: str,
    unit: str,
) -> Discipline:
    """Создать и добавить спортивную дисциплину."""
    for discipline in disciplines:
        if discipline.name.lower() == name.strip().lower():
            raise ValueError(
                "Такая дисциплина уже существует"
            )

    discipline_id = max(
        (discipline.id for discipline in disciplines),
        default=0,
    ) + 1

    discipline = Discipline(
        discipline_id=discipline_id,
        name=name,
        unit=unit,
    )

    disciplines.append(discipline)
    return discipline


def find_disciplines(
    disciplines: List[Discipline],
    query: str,
) -> List[Discipline]:
    """Найти дисциплины по названию."""
    query = query.lower().strip()

    return [
        discipline
        for discipline in disciplines
        if query in discipline.name.lower()
    ]


def sort_disciplines(
    disciplines: List[Discipline],
) -> List[Discipline]:
    """Отсортировать дисциплины по названию."""
    return sorted(
        disciplines,
        key=lambda discipline: discipline.name.lower(),
    )


def get_discipline_by_id(
    disciplines: List[Discipline],
    discipline_id: int,
) -> Optional[Discipline]:
    """Найти дисциплину по ID."""
    for discipline in disciplines:
        if discipline.id == discipline_id:
            return discipline

    return None
