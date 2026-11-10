"""Представления Sports Results на Django ORM."""

from django.core.paginator import Paginator
from django.db.models import Avg, Count, F, Min, Q
from django.shortcuts import render

from .models import Athlete, Competition, Discipline, Result


def athletes(request):
    """Список спортсменов с количеством результатов."""
    athletes_data = (
        Athlete.objects
        .annotate(results_count=Count("results"))
        .order_by("full_name")
    )

    return render(
        request,
        "sports/athlete_list.html",
        {"athletes": athletes_data},
    )


def athlete_detail(request, athlete_id):
    """Подробная информация о спортсмене."""
    try:
        athlete = Athlete.objects.get(pk=athlete_id)
    except Athlete.DoesNotExist:
        athlete = None

    athlete_results = []

    if athlete is not None:
        athlete_results = (
            athlete.results
            .select_related("discipline", "competition")
            .order_by("competition__date", "place")
        )

    return render(
        request,
        "sports/athlete_detail.html",
        {
            "athlete": athlete,
            "athlete_results": athlete_results,
        },
        status=404 if athlete is None else 200,
    )


def competitions(request):
    """Список соревнований."""
    competitions_data = (
        Competition.objects
        .annotate(results_count=Count("results"))
        .order_by("-date", "name")
    )

    return render(
        request,
        "sports/competition_list.html",
        {"competitions": competitions_data},
    )


def results(request):
    """Результаты: поиск, фильтрация, сортировка и пагинация."""
    queryset = Result.objects.select_related(
        "athlete",
        "discipline",
        "competition",
    )

    search = request.GET.get("q", "").strip()
    place = request.GET.get("place", "").strip()
    discipline_id = request.GET.get("discipline", "").strip()
    competition_id = request.GET.get("competition", "").strip()
    standard = request.GET.get("standard", "").strip()
    sort = request.GET.get("sort", "place").strip()

    if search:
        queryset = queryset.filter(
            Q(athlete__full_name__icontains=search)
            | Q(discipline__name__icontains=search)
            | Q(competition__name__icontains=search)
        )

    if place.isdigit():
        queryset = queryset.filter(place=int(place))

    if discipline_id.isdigit():
        queryset = queryset.filter(
            discipline_id=int(discipline_id)
        )

    if competition_id.isdigit():
        queryset = queryset.filter(
            competition_id=int(competition_id)
        )

    if standard == "yes":
        queryset = queryset.filter(
            result__lte=F("standard")
        )
    elif standard == "no":
        queryset = queryset.exclude(
            result__lte=F("standard")
        )

    sorting = {
        "place": ("place", "result", "id"),
        "result": ("result", "id"),
        "-result": ("-result", "id"),
        "athlete": ("athlete__full_name", "id"),
        "date": ("-competition__date", "id"),
    }

    if sort not in sorting:
        sort = "place"

    queryset = queryset.order_by(*sorting[sort])

    paginator = Paginator(queryset, 5)
    page_obj = paginator.get_page(
        request.GET.get("page")
    )

    return render(
        request,
        "sports/result_list.html",
        {
            "results": page_obj,
            "page_obj": page_obj,
            "total_count": paginator.count,
            "search": search,
            "place": place,
            "discipline_id": discipline_id,
            "competition_id": competition_id,
            "standard": standard,
            "sort": sort,
            "disciplines": Discipline.objects.all(),
            "competitions": Competition.objects.all(),
        },
    )


def result_detail(request, result_id):
    """Подробная информация о результате."""
    try:
        result = (
            Result.objects
            .select_related(
                "athlete",
                "discipline",
                "competition",
            )
            .get(pk=result_id)
        )
    except Result.DoesNotExist:
        result = None

    return render(
        request,
        "sports/result_detail.html",
        {"result": result},
        status=404 if result is None else 200,
    )


def athlete_search(request):
    """Поиск спортсменов по имени и году рождения."""
    birth_year = request.GET.get("birth_year", "").strip()
    name = request.GET.get("name", "").strip()

    athletes_data = Athlete.objects.all()
    searched = bool(birth_year or name)
    error = ""

    if name:
        athletes_data = athletes_data.filter(
            full_name__icontains=name
        )

    if birth_year:
        if birth_year.isdigit() and 1900 <= int(birth_year) <= 2100:
            athletes_data = athletes_data.filter(
                birth_year__gte=int(birth_year)
            )
        else:
            error = "Укажите корректный год рождения."
            athletes_data = athletes_data.none()

    athletes_data = athletes_data.order_by(
        "birth_year",
        "full_name",
    )

    return render(
        request,
        "sports/athlete_search.html",
        {
            "athletes": athletes_data if searched else [],
            "birth_year": birth_year,
            "name": name,
            "searched": searched,
            "error": error,
        },
    )


def statistics(request):
    """Статистика по дисциплинам средствами ORM."""
    statistics_data = (
        Discipline.objects
        .annotate(
            results_count=Count("results"),
            best_result=Min("results__result"),
            average_result=Avg("results__result"),
        )
        .order_by("-results_count", "name")
    )

    overall = Result.objects.aggregate(
        total_results=Count("id"),
        average_result=Avg("result"),
    )

    return render(
        request,
        "sports/statistics.html",
        {
            "statistics": statistics_data,
            "overall": overall,
        },
    )
