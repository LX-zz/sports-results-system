from disciplines import add_discipline, find_disciplines
from models import Discipline


def test_add_and_find_discipline():
    disciplines = []

    discipline = add_discipline(
        disciplines,
        "Бег 100 метров",
        "сек.",
    )

    found = find_disciplines(
        disciplines,
        "100",
    )

    assert len(disciplines) == 1
    assert isinstance(discipline, Discipline)
    assert len(found) == 1
    assert found[0].name == "Бег 100 метров"
