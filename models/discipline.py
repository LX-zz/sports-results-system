class Discipline:

    def __init__(
        self,
        discipline_id: int,
        name: str,
        unit: str,
    ) -> None:
        if not name.strip():
            raise ValueError("Название дисциплины не может быть пустым")

        if not unit.strip():
            raise ValueError("Единица измерения не может быть пустой")

        self.id = discipline_id
        self.name = name.strip()
        self.unit = unit.strip()

    def __str__(self) -> str:
        return f"{self.id}. {self.name} | " f"{self.unit}"

    @classmethod
    def from_data(
        cls,
        data: dict,
    ) -> "Discipline":
        return cls(
            discipline_id=data["id"],
            name=data["name"],
            unit=data["unit"],
        )

    def to_data(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "unit": self.unit,
        }
