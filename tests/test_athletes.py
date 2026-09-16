from athletes import (
    add_athlete,
    find_athletes,
)


def test_add_athlete():
    athletes = []

    add_athlete(
        athletes,
        "Иван Иванов",
        2004,
    )

    assert len(athletes) == 1


def test_find_athlete():
    athletes = [
        {
            "id": 1,
            "full_name": "Иван Иванов",
            "birth_year": 2004,
        }
    ]

    result = find_athletes(
        athletes,
        "Иван",
    )

    assert len(result) == 1