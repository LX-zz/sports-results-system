def add_athlete(
    athletes: list[dict],
    full_name: str,
    birth_year: int,
) -> dict:
    """Добавить нового спортсмена."""
    if not full_name.strip():
        raise ValueError("Имя спортсмена не может быть пустым")

    if birth_year < 1900 or birth_year > 2026:
        raise ValueError("Некорректный год рождения")

    athlete = {
        "id": max(
            (item["id"] for item in athletes),
            default=0
        ) + 1,
        "full_name": full_name.strip(),
        "birth_year": birth_year,
    }

    athletes.append(athlete)
    return athlete


def find_athletes(
    athletes: list[dict],
    query: str,
) -> list[dict]:
    """Найти спортсменов по имени."""
    query = query.lower().strip()

    return [
        athlete
        for athlete in athletes
        if query in athlete["full_name"].lower()
    ]


def sort_athletes(
    athletes: list[dict],
) -> list[dict]:
    """Отсортировать спортсменов по имени."""
    return sorted(
        athletes,
        key=lambda athlete: athlete["full_name"].lower()
    )


def get_athlete_by_id(
    athletes: list[dict],
    athlete_id: int,
):
    """Найти спортсмена по ID."""
    for athlete in athletes:
        if athlete["id"] == athlete_id:
            return athlete

    return None
