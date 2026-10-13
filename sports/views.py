"""View-функции спортивной части проекта."""

from django.http import Http404, HttpResponse

from storage import (
    load_athletes,
    load_competitions,
    load_disciplines,
    load_results,
)


ATHLETES_FILE = "data/athletes.json"
DISCIPLINES_FILE = "data/disciplines.json"
COMPETITIONS_FILE = "data/competitions.json"
RESULTS_FILE = "data/results.json"


def page(
    title: str,
    content: str,
) -> str:
    """Сформировать HTML-страницу."""
    return f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <title>{title}</title>
        <link
          href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
          rel="stylesheet">
    </head>
    <body>
        <nav class="navbar navbar-dark bg-dark">
            <div class="container">
                <a class="navbar-brand" href="/">
                    Sports Results
                </a>

                <div>
                    <a class="btn btn-outline-light"
                       href="/athletes/">
                        Спортсмены
                    </a>

                    <a class="btn btn-outline-light"
                       href="/results/">
                        Результаты
                    </a>

                    <a class="btn btn-outline-light"
                       href="/competitions/">
                        Соревнования
                    </a>
                </div>
            </div>
        </nav>

        <main class="container py-4">
            {content}
        </main>
    </body>
    </html>
    """


def get_project_data():
    """Загрузить данные предметной области."""
    athletes_list = load_athletes(
        ATHLETES_FILE
    )

    disciplines_list = load_disciplines(
        DISCIPLINES_FILE
    )

    competitions_list = load_competitions(
        COMPETITIONS_FILE
    )

    results_list = load_results(
        RESULTS_FILE,
        athletes_list,
        disciplines_list,
        competitions_list,
    )

    return (
        athletes_list,
        disciplines_list,
        competitions_list,
        results_list,
    )


def athletes(request):
    """Отобразить список спортсменов."""
    athletes_list, _, _, _ = get_project_data()

    items = ""

    for athlete in athletes_list:
        items += f"""
        <tr>
            <td>{athlete.id}</td>
            <td>
                <a href="/athletes/{athlete.id}/">
                    {athlete.full_name}
                </a>
            </td>
            <td>{athlete.birth_year}</td>
        </tr>
        """

    content = f"""
    <h1 class="mb-4">Спортсмены</h1>

    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>ФИО</th>
                <th>Год рождения</th>
            </tr>
        </thead>
        <tbody>
            {items}
        </tbody>
    </table>
    """

    return HttpResponse(
        page(
            "Спортсмены",
            content,
        )
    )


def athlete_detail(
    request,
    athlete_id: int,
):
    """Отобразить страницу спортсмена."""
    athletes_list, _, _, results_list = get_project_data()

    athlete = next(
        (
            item
            for item in athletes_list
            if item.id == athlete_id
        ),
        None,
    )

    if athlete is None:
        raise Http404(
            "Спортсмен не найден"
        )

    athlete_results = [
        result
        for result in results_list
        if result.athlete.id == athlete.id
    ]

    result_items = ""

    for result in athlete_results:
        result_items += f"""
        <li class="list-group-item">
            {result.discipline.name}:
            {result.value} {result.discipline.unit},
            место {result.place}
        </li>
        """

    if not result_items:
        result_items = """
        <li class="list-group-item">
            Результаты отсутствуют
        </li>
        """

    content = f"""
    <h1>{athlete.full_name}</h1>

    <p>
        <strong>ID:</strong>
        {athlete.id}
    </p>

    <p>
        <strong>Год рождения:</strong>
        {athlete.birth_year}
    </p>

    <h2 class="mt-4">
        Результаты спортсмена
    </h2>

    <ul class="list-group">
        {result_items}
    </ul>
    """

    return HttpResponse(
        page(
            athlete.full_name,
            content,
        )
    )


def competitions(request):
    """Отобразить список соревнований."""
    _, _, competitions_list, _ = get_project_data()

    items = ""

    for competition in competitions_list:
        items += f"""
        <tr>
            <td>{competition.id}</td>
            <td>{competition.name}</td>
            <td>{competition.date}</td>
        </tr>
        """

    content = f"""
    <h1 class="mb-4">Соревнования</h1>

    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Название</th>
                <th>Дата</th>
            </tr>
        </thead>
        <tbody>
            {items}
        </tbody>
    </table>
    """

    return HttpResponse(
        page(
            "Соревнования",
            content,
        )
    )


def results(request):
    """Отобразить список результатов."""
    _, _, _, results_list = get_project_data()

    items = ""

    for result in results_list:
        status = (
            "Норматив выполнен"
            if result.check_standard()
            else "Норматив не выполнен"
        )

        items += f"""
        <tr>
            <td>{result.id}</td>
            <td>{result.athlete.full_name}</td>
            <td>{result.discipline.name}</td>
            <td>{result.competition.name}</td>
            <td>
                <a href="/results/{result.id}/">
                    {result.value}
                    {result.discipline.unit}
                </a>
            </td>
            <td>{result.place}</td>
            <td>{status}</td>
        </tr>
        """

    content = f"""
    <h1 class="mb-4">
        Спортивные результаты
    </h1>

    <table class="table table-striped">
        <thead>
            <tr>
                <th>ID</th>
                <th>Спортсмен</th>
                <th>Дисциплина</th>
                <th>Соревнование</th>
                <th>Результат</th>
                <th>Место</th>
                <th>Норматив</th>
            </tr>
        </thead>
        <tbody>
            {items}
        </tbody>
    </table>
    """

    return HttpResponse(
        page(
            "Результаты",
            content,
        )
    )


def result_detail(
    request,
    result_id: int,
):
    """Отобразить отдельный результат."""
    _, _, _, results_list = get_project_data()

    result = next(
        (
            item
            for item in results_list
            if item.id == result_id
        ),
        None,
    )

    if result is None:
        raise Http404(
            "Результат не найден"
        )

    standard_status = (
        "Норматив выполнен"
        if result.check_standard()
        else "Норматив не выполнен"
    )

    content = f"""
    <h1>Результат №{result.id}</h1>

    <div class="card mt-4">
        <div class="card-body">
            <p>
                <strong>Спортсмен:</strong>
                {result.athlete.full_name}
            </p>

            <p>
                <strong>Дисциплина:</strong>
                {result.discipline.name}
            </p>

            <p>
                <strong>Соревнование:</strong>
                {result.competition.name}
            </p>

            <p>
                <strong>Результат:</strong>
                {result.value}
                {result.discipline.unit}
            </p>

            <p>
                <strong>Место:</strong>
                {result.place}
            </p>

            <p>
                <strong>Статус:</strong>
                {result.get_place_status()}
            </p>

            <p>
                <strong>Норматив:</strong>
                {standard_status}
            </p>
        </div>
    </div>
    """

    return HttpResponse(
        page(
            f"Результат №{result.id}",
            content,
        )
    )
