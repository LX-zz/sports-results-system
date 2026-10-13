"""View-функции главной страницы."""

from django.http import HttpResponse


def index(request):
    """Отобразить главную страницу."""
    html = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, initial-scale=1">
        <title>Система учета спортивных результатов</title>
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
            <div class="p-5 bg-light rounded-3">
                <h1>Система учета спортивных результатов</h1>

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
        </main>
    </body>
    </html>
    """

    return HttpResponse(html)
