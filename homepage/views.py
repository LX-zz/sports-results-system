"""View-функции главной страницы."""

from django.shortcuts import render


def index(request):
    """Отобразить главную страницу."""
    return render(
        request,
        "homepage/index.html",
    )


def page_not_found(
    request,
    exception,
):
    """Отобразить страницу ошибки 404."""
    return render(
        request,
        "homepage/404.html",
        status=404,
    )
