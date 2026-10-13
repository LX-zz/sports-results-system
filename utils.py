def input_int(
    prompt: str,
) -> int:
    while True:
        try:
            return int(input(prompt))

        except ValueError:
            print("Ошибка: введите целое число")


def input_float(
    prompt: str,
) -> float:
    while True:
        try:
            value = float(input(prompt))

            if value <= 0:
                raise ValueError

            return value

        except ValueError:
            print("Ошибка: введите " "число больше нуля")
