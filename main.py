from athletes import (
    add_athlete,
    find_athletes,
    get_athlete_by_id,
    sort_athletes,
)

from results import (
    add_result,
    check_result,
    check_standard,
    delete_result,
    find_results,
    get_place_status,
    get_statistics,
    sort_results,
)

from storage import (
    load_json,
    save_json,
)

from utils import (
    input_float,
    input_int,
)


ATHLETES_FILE = "data/athletes.json"
RESULTS_FILE = "data/results.json"


def show_athletes(
    athletes: list[dict],
) -> None:
    """Вывести спортсменов."""
    if not athletes:
        print("Список спортсменов пуст")
        return

    print("\nСпортсмены:")

    for athlete in sort_athletes(athletes):
        print(
            f'{athlete["id"]}. '
            f'{athlete["full_name"]} | '
            f'{athlete["birth_year"]} г.р.'
        )


def show_results(
    results: list[dict],
    athletes: list[dict],
) -> None:
    """Вывести результаты."""
    if not results:
        print("Список результатов пуст")
        return

    print("\nРезультаты:")

    for item in sort_results(results):
        athlete = get_athlete_by_id(
            athletes,
            item["athlete_id"],
        )

        if athlete:
            athlete_name = athlete["full_name"]
        else:
            athlete_name = "Неизвестный спортсмен"

        print(
            f'{item["id"]}. '
            f'{athlete_name} | '
            f'{item["discipline"]} | '
            f'{item["competition"]} | '
            f'{item["result"]} сек. | '
            f'место {item["place"]}'
        )


def create_athlete(
    athletes: list[dict],
) -> None:
    """Добавить спортсмена."""
    full_name = input(
        "ФИО спортсмена: "
    )

    birth_year = input_int(
        "Год рождения: "
    )

    try:
        athlete = add_athlete(
            athletes,
            full_name,
            birth_year,
        )

    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    save_json(
        ATHLETES_FILE,
        athletes,
    )

    print(
        f'Спортсмен '
        f'{athlete["full_name"]} добавлен'
    )


def create_result(
    results: list[dict],
    athletes: list[dict],
) -> None:
    """Добавить результат."""
    show_athletes(athletes)

    athlete_id = input_int(
        "ID спортсмена: "
    )

    athlete = get_athlete_by_id(
        athletes,
        athlete_id,
    )

    if athlete is None:
        print(
            "Спортсмен с таким ID "
            "не найден"
        )
        return

    discipline = input(
        "Дисциплина: "
    )

    competition = input(
        "Соревнование: "
    )

    result = input_float(
        "Результат в секундах: "
    )

    place = input_int(
        "Занятое место: "
    )

    standard = input_float(
        "Норматив в секундах: "
    )

    try:
        new_result = add_result(
            results,
            athlete_id,
            discipline,
            competition,
            result,
            place,
            standard,
        )

    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    save_json(
        RESULTS_FILE,
        results,
    )

    print(
        check_result(
            new_result["result"]
        )
    )

    print(
        get_place_status(
            new_result["place"]
        )
    )

    print(
        check_standard(
            new_result["result"],
            new_result["standard"],
        )
    )


def search_athletes(
    athletes: list[dict],
) -> None:
    """Найти спортсмена."""
    query = input(
        "Введите часть имени: "
    )

    found = find_athletes(
        athletes,
        query,
    )

    show_athletes(found)


def search_results(
    results: list[dict],
    athletes: list[dict],
) -> None:
    """Найти спортивный результат."""
    query = input(
        "Введите дисциплину "
        "или соревнование: "
    )

    found = find_results(
        results,
        query,
    )

    show_results(
        found,
        athletes,
    )


def remove_result(
    results: list[dict],
) -> None:
    """Удалить результат."""
    result_id = input_int(
        "ID результата: "
    )

    if delete_result(
        results,
        result_id,
    ):
        save_json(
            RESULTS_FILE,
            results,
        )

        print("Результат удален")

    else:
        print(
            "Результат с таким ID "
            "не найден"
        )


def show_statistics(
    results: list[dict],
) -> None:
    """Показать статистику."""
    statistics = get_statistics(
        results
    )

    if statistics["count"] == 0:
        print(
            "Нет данных для статистики"
        )
        return

    print(
        "Количество результатов:",
        statistics["count"],
    )

    print(
        "Лучший результат:",
        statistics["best_result"],
        "сек.",
    )

    print(
        "Средний результат:",
        round(
            statistics["average_result"],
            2,
        ),
        "сек.",
    )


def print_menu() -> None:
    """Вывести главное меню."""
    print(
        "\n=== Система учета "
        "спортивных результатов ==="
    )

    print("1. Показать спортсменов")
    print("2. Добавить спортсмена")
    print("3. Найти спортсмена")
    print("4. Показать результаты")
    print("5. Добавить результат")
    print("6. Найти результат")
    print("7. Удалить результат")
    print("8. Показать статистику")
    print("0. Выход")


def main() -> None:
    """Запустить программу."""
    athletes = load_json(
        ATHLETES_FILE
    )

    results = load_json(
        RESULTS_FILE
    )

    while True:
        print_menu()

        choice = input(
            "Выберите действие: "
        ).strip()

        if choice == "1":
            show_athletes(athletes)

        elif choice == "2":
            create_athlete(athletes)

        elif choice == "3":
            search_athletes(athletes)

        elif choice == "4":
            show_results(
                results,
                athletes,
            )

        elif choice == "5":
            create_result(
                results,
                athletes,
            )

        elif choice == "6":
            search_results(
                results,
                athletes,
            )

        elif choice == "7":
            remove_result(results)

        elif choice == "8":
            show_statistics(results)

        elif choice == "0":
            print(
                "Работа программы завершена"
            )
            break

        else:
            print(
                "Неизвестный пункт меню"
            )


if __name__ == "__main__":
    main()