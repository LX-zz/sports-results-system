from athletes import (
    add_athlete,
    get_athlete_by_id,
    sort_athletes,
)

from competitions import (
    add_competition,
    get_competition_by_id,
    sort_competitions,
)

from disciplines import (
    add_discipline,
    get_discipline_by_id,
    sort_disciplines,
)

from results import (
    add_result,
    check_result,
    check_standard,
    delete_result,
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
DISCIPLINES_FILE = "data/disciplines.json"
COMPETITIONS_FILE = "data/competitions.json"
RESULTS_FILE = "data/results.json"


def show_athletes(
    athletes: list[dict],
) -> None:
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


def show_disciplines(
    disciplines: list[dict],
) -> None:
    if not disciplines:
        print("Список дисциплин пуст")
        return

    print("\nДисциплины:")

    for discipline in sort_disciplines(disciplines):
        print(
            f'{discipline["id"]}. '
            f'{discipline["name"]} | '
            f'{discipline["unit"]}'
        )


def show_competitions(
    competitions: list[dict],
) -> None:
    if not competitions:
        print("Список соревнований пуст")
        return

    print("\nСоревнования:")

    for competition in sort_competitions(competitions):
        print(
            f'{competition["id"]}. '
            f'{competition["name"]} | '
            f'{competition["date"]}'
        )


def show_results(
    results: list[dict],
    athletes: list[dict],
    disciplines: list[dict],
    competitions: list[dict],
) -> None:
    if not results:
        print("Список результатов пуст")
        return

    print("\nРезультаты:")

    for item in sort_results(results):
        athlete = get_athlete_by_id(
            athletes,
            item["athlete_id"],
        )

        discipline = get_discipline_by_id(
            disciplines,
            item["discipline_id"],
        )

        competition = get_competition_by_id(
            competitions,
            item["competition_id"],
        )

        athlete_name = (
            athlete["full_name"]
            if athlete
            else "Неизвестный спортсмен"
        )

        discipline_name = (
            discipline["name"]
            if discipline
            else "Неизвестная дисциплина"
        )

        competition_name = (
            competition["name"]
            if competition
            else "Неизвестное соревнование"
        )

        print(
            f'{item["id"]}. '
            f'{athlete_name} | '
            f'{discipline_name} | '
            f'{competition_name} | '
            f'{item["result"]} | '
            f'место {item["place"]}'
        )


def create_athlete(
    athletes: list[dict],
) -> None:
    full_name = input("ФИО спортсмена: ")
    birth_year = input_int("Год рождения: ")

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
        f'Спортсмен {athlete["full_name"]} добавлен'
    )


def create_discipline(
    disciplines: list[dict],
) -> None:
    name = input("Название дисциплины: ")
    unit = input("Единица измерения: ")

    try:
        discipline = add_discipline(
            disciplines,
            name,
            unit,
        )

    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    save_json(
        DISCIPLINES_FILE,
        disciplines,
    )

    print(
        f'Дисциплина {discipline["name"]} добавлена'
    )


def create_competition(
    competitions: list[dict],
) -> None:
    name = input("Название соревнования: ")
    date = input("Дата в формате ГГГГ-ММ-ДД: ")

    try:
        competition = add_competition(
            competitions,
            name,
            date,
        )

    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    save_json(
        COMPETITIONS_FILE,
        competitions,
    )

    print(
        f'Соревнование {competition["name"]} добавлено'
    )


def create_result(
    results: list[dict],
    athletes: list[dict],
    disciplines: list[dict],
    competitions: list[dict],
) -> None:
    show_athletes(athletes)
    athlete_id = input_int("ID спортсмена: ")

    if get_athlete_by_id(
        athletes,
        athlete_id,
    ) is None:
        print("Спортсмен не найден")
        return

    show_disciplines(disciplines)
    discipline_id = input_int("ID дисциплины: ")

    if get_discipline_by_id(
        disciplines,
        discipline_id,
    ) is None:
        print("Дисциплина не найдена")
        return

    show_competitions(competitions)
    competition_id = input_int("ID соревнования: ")

    if get_competition_by_id(
        competitions,
        competition_id,
    ) is None:
        print("Соревнование не найдено")
        return

    result = input_float("Результат: ")
    place = input_int("Занятое место: ")
    standard = input_float("Норматив: ")

    try:
        new_result = add_result(
            results,
            athlete_id,
            discipline_id,
            competition_id,
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

    print(check_result(new_result["result"]))
    print(get_place_status(new_result["place"]))
    print(
        check_standard(
            new_result["result"],
            new_result["standard"],
        )
    )


def remove_result(
    results: list[dict],
) -> None:
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
        print("Результат не найден")


def show_statistics(
    results: list[dict],
) -> None:
    statistics = get_statistics(
        results
    )

    if statistics["count"] == 0:
        print("Нет данных для статистики")
        return

    print(
        "Количество результатов:",
        statistics["count"],
    )

    print(
        "Лучший результат:",
        statistics["best_result"],
    )

    print(
        "Средний результат:",
        round(
            statistics["average_result"],
            2,
        ),
    )


def print_menu() -> None:
    print(
        "\n=== Система учета "
        "спортивных результатов ==="
    )

    print("1. Показать спортсменов")
    print("2. Добавить спортсмена")
    print("3. Показать дисциплины")
    print("4. Добавить дисциплину")
    print("5. Показать соревнования")
    print("6. Добавить соревнование")
    print("7. Показать результаты")
    print("8. Добавить результат")
    print("9. Удалить результат")
    print("10. Показать статистику")
    print("0. Выход")


def main() -> None:
    athletes = load_json(
        ATHLETES_FILE
    )

    disciplines = load_json(
        DISCIPLINES_FILE
    )

    competitions = load_json(
        COMPETITIONS_FILE
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
            show_disciplines(disciplines)

        elif choice == "4":
            create_discipline(disciplines)

        elif choice == "5":
            show_competitions(competitions)

        elif choice == "6":
            create_competition(competitions)

        elif choice == "7":
            show_results(
                results,
                athletes,
                disciplines,
                competitions,
            )

        elif choice == "8":
            create_result(
                results,
                athletes,
                disciplines,
                competitions,
            )

        elif choice == "9":
            remove_result(results)

        elif choice == "10":
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
