from competitions import (
    add_competition,
    find_competitions,
)


def test_add_and_find_competition():
    competitions = []

    add_competition(
        competitions,
        "Кубок РТУ МИРЭА",
        "2026-09-20",
    )

    found = find_competitions(
        competitions,
        "МИРЭА",
    )

    assert len(competitions) == 1
    assert len(found) == 1
