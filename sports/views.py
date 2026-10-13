"""View-функции спортивной части проекта."""

from django.shortcuts import render

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

    context = {
        "athletes": athletes_list,
    }

    return render(
        request,
        "sports/athlete_list.html",
        context,
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

    athlete_results = []

    if athlete is not None:
        athlete_results = [
            result
            for result in results_list
            if result.athlete.id == athlete.id
        ]

    context = {
        "athlete": athlete,
        "athlete_results": athlete_results,
    }

    return render(
        request,
        "sports/athlete_detail.html",
        context,
        status=404 if athlete is None else 200,
    )


def competitions(request):
    """Отобразить список соревнований."""
    _, _, competitions_list, _ = get_project_data()

    context = {
        "competitions": competitions_list,
    }

    return render(
        request,
        "sports/competition_list.html",
        context,
    )


def results(request):
    """Отобразить список результатов."""
    _, _, _, results_list = get_project_data()

    context = {
        "results": results_list,
    }

    return render(
        request,
        "sports/result_list.html",
        context,
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

    context = {
        "result": result,
    }

    return render(
        request,
        "sports/result_detail.html",
        context,
        status=404 if result is None else 200,
    )
