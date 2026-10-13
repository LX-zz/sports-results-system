from typing import List

from models import Athlete, Competition, Discipline, Result


def add_result(
    results: List[Result],
    athlete: Athlete,
    discipline: Discipline,
    competition: Competition,
    value: float,
    place: int,
    standard: float,
) -> Result:
    """Создать и добавить спортивный результат."""
    for item in results:
        if (
            item.athlete.id == athlete.id
            and item.discipline.id == discipline.id
            and item.competition.id == competition.id
        ):
            raise ValueError("Такой результат уже существует")

    result_id = (
        max(
            (item.id for item in results),
            default=0,
        )
        + 1
    )

    result = Result(
        result_id=result_id,
        athlete=athlete,
        discipline=discipline,
        competition=competition,
        value=value,
        place=place,
        standard=standard,
    )

    results.append(result)
    return result


def delete_result(
    results: List[Result],
    result_id: int,
) -> bool:
    """Удалить результат по ID."""
    for index, result in enumerate(results):
        if result.id == result_id:
            del results[index]
            return True

    return False


def find_results(
    results: List[Result],
    discipline_id: int,
) -> List[Result]:
    """Найти результаты по дисциплине."""
    return [result for result in results if result.discipline.id == discipline_id]


def sort_results(
    results: List[Result],
) -> List[Result]:
    """Отсортировать результаты."""
    return sorted(
        results,
        key=lambda result: result.value,
    )


def get_statistics(
    results: List[Result],
) -> dict:
    """Получить статистику результатов."""
    if not results:
        return {
            "count": 0,
            "best_result": None,
            "average_result": None,
        }

    values = [result.value for result in results]

    return {
        "count": len(values),
        "best_result": min(values),
        "average_result": sum(values) / len(values),
    }
