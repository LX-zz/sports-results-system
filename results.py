def check_result(result: float) -> str:
    """Проверить корректность результата."""
    if result > 0:
        return "Результат корректный"

    return "Ошибка: результат должен быть больше 0"


def get_place_status(place: int) -> str:
    """Определить статус спортсмена по месту."""
    if place == 1:
        return "Золотая медаль"

    if place == 2:
        return "Серебряная медаль"

    if place == 3:
        return "Бронзовая медаль"

    return "Участник соревнования"


def check_standard(
    result: float,
    standard: float,
) -> str:
    """Проверить выполнение норматива."""
    if result <= standard:
        return "Норматив выполнен"

    return "Норматив не выполнен"


def is_result_unique(
    results: list[dict],
    athlete_id: int,
    discipline: str,
    competition: str,
) -> bool:
    """Проверить отсутствие повторного результата."""
    for item in results:
        same_athlete = item["athlete_id"] == athlete_id

        same_discipline = (
            item["discipline"].lower()
            == discipline.lower().strip()
        )

        same_competition = (
            item["competition"].lower()
            == competition.lower().strip()
        )

        if (
            same_athlete
            and same_discipline
            and same_competition
        ):
            return False

    return True


def add_result(
    results: list[dict],
    athlete_id: int,
    discipline: str,
    competition: str,
    result: float,
    place: int,
    standard: float,
) -> dict:
    """Добавить спортивный результат."""
    if result <= 0:
        raise ValueError(
            "Результат должен быть больше нуля"
        )

    if standard <= 0:
        raise ValueError(
            "Норматив должен быть больше нуля"
        )

    if place <= 0:
        raise ValueError(
            "Место должно быть больше нуля"
        )

    if not discipline.strip():
        raise ValueError(
            "Дисциплина не может быть пустой"
        )

    if not competition.strip():
        raise ValueError(
            "Соревнование не может быть пустым"
        )

    if not is_result_unique(
        results,
        athlete_id,
        discipline,
        competition,
    ):
        raise ValueError(
            "Такой результат уже существует"
        )

    new_result = {
        "id": max(
            (item["id"] for item in results),
            default=0
        ) + 1,
        "athlete_id": athlete_id,
        "discipline": discipline.strip(),
        "competition": competition.strip(),
        "result": result,
        "place": place,
        "standard": standard,
    }

    results.append(new_result)

    return new_result


def delete_result(
    results: list[dict],
    result_id: int,
) -> bool:
    """Удалить результат по ID."""
    for index, item in enumerate(results):
        if item["id"] == result_id:
            del results[index]
            return True

    return False


def find_results(
    results: list[dict],
    query: str,
) -> list[dict]:
    """Найти результаты по дисциплине или соревнованию."""
    query = query.lower().strip()

    return [
        item
        for item in results
        if (
            query in item["discipline"].lower()
            or query in item["competition"].lower()
        )
    ]


def sort_results(
    results: list[dict],
) -> list[dict]:
    """Отсортировать результаты от лучшего к худшему."""
    return sorted(
        results,
        key=lambda item: item["result"]
    )


def get_statistics(
    results: list[dict],
) -> dict:
    """Получить статистику результатов."""
    if not results:
        return {
            "count": 0,
            "best_result": None,
            "average_result": None,
        }

    values = [
        item["result"]
        for item in results
    ]

    return {
        "count": len(values),
        "best_result": min(values),
        "average_result": sum(values) / len(values),
    }