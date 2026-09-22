import pytest

from models import (
    Athlete,
    Competition,
    Discipline,
)
from results import (
    add_result,
    get_statistics,
)


def create_objects():
    athlete = Athlete(
        1,
        "Иван Иванов",
        2005,
    )

    discipline = Discipline(
        1,
        "Бег 100 метров",
        "сек.",
    )

    competition = Competition(
        1,
        "Кубок РТУ МИРЭА",
        "2026-09-20",
    )

    return athlete, discipline, competition


def test_add_result():
    results = []

    athlete, discipline, competition = create_objects()

    result = add_result(
        results,
        athlete,
        discipline,
        competition,
        11.8,
        1,
        12.0,
    )

    assert len(results) == 1
    assert result.athlete is athlete


def test_duplicate_result():
    results = []

    athlete, discipline, competition = create_objects()

    add_result(
        results,
        athlete,
        discipline,
        competition,
        11.8,
        1,
        12.0,
    )

    with pytest.raises(ValueError):
        add_result(
            results,
            athlete,
            discipline,
            competition,
            11.9,
            2,
            12.0,
        )


def test_statistics():
    results = []

    athlete, discipline, competition = create_objects()

    add_result(
        results,
        athlete,
        discipline,
        competition,
        11.5,
        1,
        12.0,
    )

    second_athlete = Athlete(
        2,
        "Петр Петров",
        2004,
    )

    add_result(
        results,
        second_athlete,
        discipline,
        competition,
        12.5,
        2,
        13.0,
    )

    statistics = get_statistics(
        results
    )

    assert statistics["count"] == 2
    assert statistics["best_result"] == 11.5
    assert statistics["average_result"] == 12.0
