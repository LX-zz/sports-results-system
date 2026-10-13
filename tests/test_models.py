import pytest

from models import Athlete, Competition, Discipline, Result


def test_athlete_creation():
    athlete = Athlete(
        1,
        "Иван Иванов",
        2005,
    )

    assert athlete.id == 1
    assert athlete.full_name == "Иван Иванов"
    assert athlete.birth_year == 2005


def test_athlete_str():
    athlete = Athlete(
        1,
        "Иван Иванов",
        2005,
    )

    assert str(athlete) == ("1. Иван Иванов | 2005 г.р.")


def test_discipline_creation():
    discipline = Discipline(
        1,
        "Бег 100 метров",
        "сек.",
    )

    assert discipline.id == 1
    assert discipline.name == "Бег 100 метров"
    assert discipline.unit == "сек."


def test_competition_creation():
    competition = Competition(
        1,
        "Кубок РТУ МИРЭА",
        "2026-09-20",
    )

    assert competition.id == 1
    assert competition.name == "Кубок РТУ МИРЭА"
    assert competition.date == "2026-09-20"


def test_result_interaction():
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

    result = Result(
        1,
        athlete,
        discipline,
        competition,
        11.7,
        2,
        12.0,
    )

    assert result.athlete is athlete
    assert result.discipline is discipline
    assert result.competition is competition


def test_result_standard():
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

    result = Result(
        1,
        athlete,
        discipline,
        competition,
        11.7,
        2,
        12.0,
    )

    assert result.check_standard() is True


def test_result_place_status():
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

    result = Result(
        1,
        athlete,
        discipline,
        competition,
        11.7,
        2,
        12.0,
    )

    assert result.get_place_status() == "Серебряная медаль"


def test_invalid_athlete():
    with pytest.raises(ValueError):
        Athlete(
            1,
            "",
            2005,
        )


def test_invalid_result():
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

    with pytest.raises(ValueError):
        Result(
            1,
            athlete,
            discipline,
            competition,
            -1.0,
            1,
            12.0,
        )
