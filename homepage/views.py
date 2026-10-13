"""View-функции главной страницы."""

from django.http import HttpResponse


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

        <main class="container py-5">
            {content}
        </main>
    </body>
    </html>
    """


def index(request):
    """Отобразить главную страницу."""
    content = """
    <div class="p-5 bg-light rounded-3">
        <h1>
            Система учета спортивных результатов
        </h1>

        <p class="lead">
            Веб-интерфейс учебного проекта для учета
            спортсменов, соревнований и спортивных
            результатов.
        </p>

        <p>
            Проект использует объектную модель
            предыдущих практических работ и данные
            из JSON-файлов.
        </p>
    </div>
    """

    return HttpResponse(
        page(
            "Система учета спортивных результатов",
            content,
        )
    )


def page_not_found(
    request,
    exception,
):
    """Отобразить страницу ошибки 404."""
    content = """
    <h1 class="text-danger">
        404 – страница не найдена
    </h1>

    <p>
        Проверьте адрес или вернитесь
        на главную страницу.
    </p>

    <a href="/"
       class="btn btn-primary">
        На главную
    </a>
    """

    return HttpResponse(
        page(
            "404 – страница не найдена",
            content,
        ),
        status=404,
    )
