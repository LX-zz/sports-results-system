"""Главный модуль системы учета спортивных результатов."""

from typing import List

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
from models import (
    Athlete,
    Competition,
    Discipline,
    Result,
)
from results import (
    add_result,
    delete_result,
    get_statistics,
    sort_results,
)
from storage import (
    load_athletes,
    load_competitions,
    load_disciplines,
    load_results,
    save_objects,
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
    athletes: List[Athlete],
) -> None:
    """Вывести спортсменов."""
    if not athletes:
        print("Список спортсменов пуст")
        return

    print("\nСпортсмены:")

    for athlete in sort_athletes(athletes):
        print(athlete)


def show_disciplines(
    disciplines: List[Discipline],
) -> None:
    """Вывести спортивные дисциплины."""
    if not disciplines:
        print("Список дисциплин пуст")
        return

    print("\nДисциплины:")

    for discipline in sort_disciplines(disciplines):
        print(discipline)


def show_competitions(
    competitions: List[Competition],
) -> None:
    """Вывести соревнования."""
    if not competitions:
        print("Список соревнований пуст")
        return

    print("\nСоревнования:")

    for competition in sort_competitions(competitions):
        print(competition)


def show_results(
    results: List[Result],
) -> None:
    """Вывести спортивные результаты."""
    if not results:
        print("Список результатов пуст")
        return

    print("\nСпортивные результаты:")

    for result in sort_results(results):
        print(result)

        standard_status = (
            "Норматив выполнен"
            if result.check_standard()
            else "Норматив не выполнен"
        )

        print(
            f"   {result.get_place_status()} | "
            f"{standard_status}"
        )


def create_athlete(
    athletes: List[Athlete],
) -> None:
    """Создать спортсмена."""
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

    save_objects(
        ATHLETES_FILE,
        athletes,
    )

    print(
        f"Спортсмен добавлен: {athlete}"
    )


def create_discipline(
    disciplines: List[Discipline],
) -> None:
    """Создать спортивную дисциплину."""
    name = input(
        "Название дисциплины: "
    )

    unit = input(
        "Единица измерения: "
    )

    try:
        discipline = add_discipline(
            disciplines,
            name,
            unit,
        )

    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    save_objects(
        DISCIPLINES_FILE,
        disciplines,
    )

    print(
        f"Дисциплина добавлена: {discipline}"
    )


def create_competition(
    competitions: List[Competition],
) -> None:
    """Создать соревнование."""
    name = input(
        "Название соревнования: "
    )

    competition_date = input(
        "Дата в формате ГГГГ-ММ-ДД: "
    )

    try:
        competition = add_competition(
            competitions,
            name,
            competition_date,
        )

    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    save_objects(
        COMPETITIONS_FILE,
        competitions,
    )

    print(
        f"Соревнование добавлено: {competition}"
    )


def create_result(
    results: List[Result],
    athletes: List[Athlete],
    disciplines: List[Discipline],
    competitions: List[Competition],
) -> None:
    """Создать спортивный результат."""
    show_athletes(athletes)

    athlete_id = input_int(
        "ID спортсмена: "
    )

    athlete = get_athlete_by_id(
        athletes,
        athlete_id,
    )

    if athlete is None:
        print("Спортсмен не найден")
        return

    show_disciplines(disciplines)

    discipline_id = input_int(
        "ID дисциплины: "
    )

    discipline = get_discipline_by_id(
        disciplines,
        discipline_id,
    )

    if discipline is None:
        print("Дисциплина не найдена")
        return

    show_competitions(competitions)

    competition_id = input_int(
        "ID соревнования: "
    )

    competition = get_competition_by_id(
        competitions,
        competition_id,
    )

    if competition is None:
        print("Соревнование не найдено")
        return

    value = input_float(
        "Результат: "
    )

    place = input_int(
        "Занятое место: "
    )

    standard = input_float(
        "Норматив: "
    )

    try:
        result = add_result(
            results,
            athlete,
            discipline,
            competition,
            value,
            place,
            standard,
        )

    except ValueError as error:
        print(f"Ошибка: {error}")
        return

    save_objects(
        RESULTS_FILE,
        results,
    )

    print(
        f"Результат добавлен: {result}"
    )

    print(
        result.get_place_status()
    )

    if result.check_standard():
        print("Норматив выполнен")
    else:
        print("Норматив не выполнен")


def remove_result(
    results: List[Result],
) -> None:
    """Удалить спортивный результат."""
    result_id = input_int(
        "ID результата: "
    )

    if delete_result(
        results,
        result_id,
    ):
        save_objects(
            RESULTS_FILE,
            results,
        )

        print("Результат удален")

    else:
        print("Результат не найден")


def show_statistics(
    results: List[Result],
) -> None:
    """Вывести статистику."""
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
    """Вывести главное меню."""
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
    """Запустить приложение."""
    athletes = load_athletes(
        ATHLETES_FILE
    )

    disciplines = load_disciplines(
        DISCIPLINES_FILE
    )

    competitions = load_competitions(
        COMPETITIONS_FILE
    )

    results = load_results(
        RESULTS_FILE,
        athletes,
        disciplines,
        competitions,
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
            show_results(results)

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
