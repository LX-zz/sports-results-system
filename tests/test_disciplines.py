from disciplines import (
    add_discipline,
    find_disciplines,
)


def test_add_and_find_discipline():
    disciplines = []

    add_discipline(
        disciplines,
        "Бег 100 метров",
        "сек.",
    )

    found = find_disciplines(
        disciplines,
        "100",
    )

    assert len(disciplines) == 1
    assert len(found) == 1
    assert found[0]["name"] == "Бег 100 метров"
