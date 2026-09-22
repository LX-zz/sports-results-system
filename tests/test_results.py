import pytest

from results import (
    add_result,
    check_standard,
    get_statistics,
)


def test_check_standard():
    result = check_standard(
        11.7,
        12.0,
    )

    assert result == "Норматив выполнен"


def test_add_result():
    results = []

    add_result(
        results,
        1,
        1,
        1,
        11.8,
        1,
        12.0,
    )

    assert len(results) == 1


def test_duplicate_result():
    results = []

    add_result(
        results,
        1,
        1,
        1,
        11.8,
        1,
        12.0,
    )

    with pytest.raises(ValueError):
        add_result(
            results,
            1,
            1,
            1,
            11.9,
            2,
            12.0,
        )


def test_statistics():
    results = [
        {"result": 11.5},
        {"result": 12.5},
    ]

    statistics = get_statistics(
        results
    )

    assert statistics["count"] == 2
    assert statistics["best_result"] == 11.5
    assert statistics["average_result"] == 12.0
