import json
from pathlib import Path


def load_json(
    filename: str,
) -> list[dict]:
    """Загрузить данные из JSON-файла."""
    path = Path(filename)

    if not path.exists():
        return []

    try:
        with path.open(
            "r",
            encoding="utf-8"
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError:
        print(
            f"Ошибка: файл {filename} "
            "содержит некорректный JSON"
        )
        return []

    except OSError as error:
        print(
            f"Ошибка чтения файла: {error}"
        )
        return []

    if not isinstance(data, list):
        return []

    return data


def save_json(
    filename: str,
    data: list[dict],
) -> None:
    """Сохранить данные в JSON-файл."""
    path = Path(filename)

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    try:
        with path.open(
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )

    except OSError as error:
        print(
            f"Ошибка сохранения файла: {error}"
        )