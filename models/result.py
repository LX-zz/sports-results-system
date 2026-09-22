"""Модель спортивного результата."""

from models.athlete import Athlete
from models.competition import Competition
from models.discipline import Discipline


class Result:
    """Спортивный результат спортсмена."""

    def __init__(
        self,
        result_id: int,
        athlete: Athlete,
        discipline: Discipline,
        competition: Competition,
        value: float,
        place: int,
        standard: float,
    ) -> None:
        """Создать объект результата."""
        if value <= 0:
            raise ValueError(
                "Результат должен быть больше нуля"
            )

        if place <= 0:
            raise ValueError(
                "Место должно быть больше нуля"
            )

        if standard <= 0:
            raise ValueError(
                "Норматив должен быть больше нуля"
            )

        self.id = result_id
        self.athlete = athlete
        self.discipline = discipline
        self.competition = competition
        self.value = value
        self.place = place
        self.standard = standard

    def check_standard(self) -> bool:
        """Проверить выполнение норматива."""
        return self.value <= self.standard

    def get_place_status(self) -> str:
        """Определить статус по занятому месту."""
        if self.place == 1:
            return "Золотая медаль"

        if self.place == 2:
            return "Серебряная медаль"

        if self.place == 3:
            return "Бронзовая медаль"

        return "Участник соревнования"

    def __str__(self) -> str:
        """Вернуть строковое представление результата."""
        return (
            f"{self.id}. "
            f"{self.athlete.full_name} | "
            f"{self.discipline.name} | "
            f"{self.competition.name} | "
            f"{self.value} {self.discipline.unit} | "
            f"место {self.place}"
        )

    def to_data(self) -> dict:
        """Преобразовать результат в словарь."""
        return {
            "id": self.id,
            "athlete_id": self.athlete.id,
            "discipline_id": self.discipline.id,
            "competition_id": self.competition.id,
            "result": self.value,
            "place": self.place,
            "standard": self.standard,
        }
