class Competition:
    """Спортивное соревнование."""

    def __init__(
        self,
        competition_id: int,
        name: str,
        competition_date: str,
    ) -> None:
        """Создать объект соревнования."""
        if not name.strip():
            raise ValueError(
                "Название соревнования не может быть пустым"
            )

        if not competition_date.strip():
            raise ValueError(
                "Дата соревнования не может быть пустой"
            )

        self.id = competition_id
        self.name = name.strip()
        self.date = competition_date.strip()

    def __str__(self) -> str:
        """Вернуть строковое представление соревнования."""
        return (
            f"{self.id}. {self.name} | "
            f"{self.date}"
        )

    @classmethod
    def from_data(
        cls,
        data: dict,
    ) -> "Competition":
        """Создать соревнование из словаря."""
        return cls(
            competition_id=data["id"],
            name=data["name"],
            competition_date=data["date"],
        )

    def to_data(self) -> dict:
        """Преобразовать соревнование в словарь."""
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
        }
