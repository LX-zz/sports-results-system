"""Модель спортсмена."""


class Athlete:
    """Спортсмен системы учета результатов."""

    def __init__(
        self,
        athlete_id: int,
        full_name: str,
        birth_year: int,
    ) -> None:
        """Создать объект спортсмена."""
        if not full_name.strip():
            raise ValueError(
                "Имя спортсмена не может быть пустым"
            )

        if birth_year < 1900 or birth_year > 2026:
            raise ValueError(
                "Некорректный год рождения"
            )

        self.id = athlete_id
        self.full_name = full_name.strip()
        self.birth_year = birth_year

    def __str__(self) -> str:
        """Вернуть строковое представление спортсмена."""
        return (
            f"{self.id}. {self.full_name} | "
            f"{self.birth_year} г.р."
        )

    @classmethod
    def from_data(
        cls,
        data: dict,
    ) -> "Athlete":
        """Создать спортсмена из словаря."""
        return cls(
            athlete_id=data["id"],
            full_name=data["full_name"],
            birth_year=data["birth_year"],
        )

    def to_data(self) -> dict:
        """Преобразовать спортсмена в словарь."""
        return {
            "id": self.id,
            "full_name": self.full_name,
            "birth_year": self.birth_year,
        }
