from athletes import add_athlete, find_athletes
from models import Athlete


def test_add_athlete():
    athletes = []

    athlete = add_athlete(
        athletes,
        "Иван Иванов",
        2004,
    )

    assert len(athletes) == 1
    assert isinstance(athlete, Athlete)
    assert athlete.full_name == "Иван Иванов"
    assert athlete.birth_year == 2004


def test_find_athlete():
    athletes = [
        Athlete(
            1,
            "Иван Иванов",
            2004,
        )
    ]

    result = find_athletes(
        athletes,
        "Иван",
    )

    assert len(result) == 1
    assert result[0].full_name == "Иван Иванов"
