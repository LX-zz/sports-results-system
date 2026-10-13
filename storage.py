import json
from pathlib import Path
from typing import List

from models import Athlete, Competition, Discipline, Result


def load_json(
    filename: str,
) -> list:
    path = Path(filename)

    if not path.exists():
        return []

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError:
        print(f"Ошибка: файл {filename} " "содержит некорректный JSON")
        return []

    except OSError as error:
        print(f"Ошибка чтения файла: {error}")
        return []

    if not isinstance(data, list):
        return []

    return data


def load_athletes(
    filename: str,
) -> List[Athlete]:
    """Загрузить спортсменов из JSON."""
    data = load_json(filename)

    return [Athlete.from_data(item) for item in data]


def load_disciplines(
    filename: str,
) -> List[Discipline]:
    """Загрузить дисциплины из JSON."""
    data = load_json(filename)

    return [Discipline.from_data(item) for item in data]


def load_competitions(
    filename: str,
) -> List[Competition]:
    """Загрузить соревнования из JSON."""
    data = load_json(filename)

    return [Competition.from_data(item) for item in data]


def load_results(
    filename: str,
    athletes: List[Athlete],
    disciplines: List[Discipline],
    competitions: List[Competition],
) -> List[Result]:
    """Загрузить спортивные результаты из JSON."""
    data = load_json(filename)
    results = []

    for item in data:
        athlete = next(
            (
                athlete
                for athlete in athletes
                if athlete.id == item["athlete_id"]
            ),
            None,
        )

        discipline = next(
            (
                discipline
                for discipline in disciplines
                if discipline.id == item["discipline_id"]
            ),
            None,
        )

        competition = next(
            (
                competition
                for competition in competitions
                if competition.id == item["competition_id"]
            ),
            None,
        )

        if athlete is None or discipline is None or competition is None:
            continue

        result = Result(
            result_id=item["id"],
            athlete=athlete,
            discipline=discipline,
            competition=competition,
            value=item["result"],
            place=item["place"],
            standard=item["standard"],
        )

        results.append(result)

    return results


def save_objects(
    filename: str,
    objects: list,
) -> None:
    """Сохранить объекты в JSON-файл."""
    path = Path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = [item.to_data() for item in objects]

    try:
        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

    except OSError as error:
        print(f"Ошибка сохранения файла: {error}")
