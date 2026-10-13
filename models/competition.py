class Competition:
    def __init__(
        self,
        competition_id: int,
        name: str,
        competition_date: str,
    ) -> None:

        if not name.strip():
            raise ValueError("Название соревнования не может быть пустым")

        if not competition_date.strip():
            raise ValueError("Дата соревнования не может быть пустой")

        self.id = competition_id
        self.name = name.strip()
        self.date = competition_date.strip()

    def __str__(self) -> str:
        return f"{self.id}. {self.name} | " f"{self.date}"

    @classmethod
    def from_data(
        cls,
        data: dict,
    ) -> "Competition":
        return cls(
            competition_id=data["id"],
            name=data["name"],
            competition_date=data["date"],
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
        }
