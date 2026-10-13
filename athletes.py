from typing import List, Optional

from models import Athlete


def add_athlete(
    athletes: List[Athlete],
    full_name: str,
    birth_year: int,
) -> Athlete:
    """Создать и добавить спортсмена."""
    athlete_id = (
        max(
            (athlete.id for athlete in athletes),
            default=0,
        )
        + 1
    )

    athlete = Athlete(
        athlete_id=athlete_id,
        full_name=full_name,
        birth_year=birth_year,
    )

    athletes.append(athlete)
    return athlete


def find_athletes(
    athletes: List[Athlete],
    query: str,
) -> List[Athlete]:
    """Найти спортсменов по имени."""
    query = query.lower().strip()

    return [athlete for athlete in athletes if query in athlete.full_name.lower()]


def sort_athletes(
    athletes: List[Athlete],
) -> List[Athlete]:
    """Отсортировать спортсменов по имени."""
    return sorted(
        athletes,
        key=lambda athlete: athlete.full_name.lower(),
    )


def get_athlete_by_id(
    athletes: List[Athlete],
    athlete_id: int,
) -> Optional[Athlete]:
    """Найти спортсмена по ID."""
    for athlete in athletes:
        if athlete.id == athlete_id:
            return athlete

    return None
