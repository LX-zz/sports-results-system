from datetime import date


athlete = input("Введите имя спортсмена: ")
discipline = input("Введите дисциплину: ")
competition = input("Введите название соревнования: ")

result = float(input("Введите результат в секундах: "))
place = int(input("Введите занятое место: "))

competition_date = date(2026, 9, 20)
standard = 12.0


def check_result(result):
    if result > 0:
        return "Результат корректный"
    return "Ошибка: результат должен быть больше 0"


def get_place_status(place):
    if place == 1:
        return "Золотая медаль"
    elif place == 2:
        return "Серебряная медаль"
    elif place == 3:
        return "Бронзовая медаль"
    else:
        return "Участник соревнования"


def check_standard(result, standard):
    if result <= standard:
        return "Норматив выполнен"
    return "Норматив не выполнен"


print()
print("Спортивный результат")
print("--------------------")
print(f"Спортсмен: {athlete}")
print(f"Дисциплина: {discipline}")
print(f"Соревнование: {competition}")
print(f"Дата соревнования: {competition_date}")
print(f"Результат: {result} сек.")
print(f"Место: {place}")
print(check_result(result))
print(get_place_status(place))
print(check_standard(result, standard))