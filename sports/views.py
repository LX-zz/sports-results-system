"""View-функции спортивной части проекта."""

from django.shortcuts import render

from db.database import get_connection


def athletes(request):
    """Показать список спортсменов из SQLite."""
    conn = get_connection()

    athletes_data = conn.execute(
        """
        SELECT
            id,
            full_name,
            birth_year
        FROM athletes
        ORDER BY full_name;
        """
    ).fetchall()

    conn.close()

    return render(
        request,
        "sports/athlete_list.html",
        {
            "athletes": athletes_data,
        },
    )


def athlete_detail(request, athlete_id: int):
    """Показать спортсмена и его результаты."""
    conn = get_connection()

    athlete = conn.execute(
        """
        SELECT
            id,
            full_name,
            birth_year
        FROM athletes
        WHERE id = ?;
        """,
        (athlete_id,),
    ).fetchone()

    athlete_results = []

    if athlete is not None:
        athlete_results = conn.execute(
            """
            SELECT
                results.id,
                disciplines.name AS discipline_name,
                competitions.name AS competition_name,
                competitions.date AS competition_date,
                results.result,
                disciplines.unit,
                results.place,
                results.standard,
                CASE
                    WHEN results.result <= results.standard
                    THEN 1
                    ELSE 0
                END AS standard_met
            FROM results
            JOIN disciplines
                ON results.discipline_id = disciplines.id
            JOIN competitions
                ON results.competition_id = competitions.id
            WHERE results.athlete_id = ?
            ORDER BY competitions.date;
            """,
            (athlete_id,),
        ).fetchall()

    conn.close()

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
    """Показать список соревнований из SQLite."""
    conn = get_connection()

    competitions_data = conn.execute(
        """
        SELECT
            id,
            name,
            date
        FROM competitions
        ORDER BY date;
        """
    ).fetchall()

    conn.close()

    return render(
        request,
        "sports/competition_list.html",
        {
            "competitions": competitions_data,
        },
    )


def results(request):
    """Показать результаты со связанными данными."""
    conn = get_connection()

    results_data = conn.execute(
        """
        SELECT
            results.id,
            athletes.id AS athlete_id,
            athletes.full_name AS athlete_name,
            disciplines.name AS discipline_name,
            competitions.name AS competition_name,
            competitions.date AS competition_date,
            results.result,
            disciplines.unit,
            results.place,
            results.standard,
            CASE
                WHEN results.result <= results.standard
                THEN 1
                ELSE 0
            END AS standard_met
        FROM results
        JOIN athletes
            ON results.athlete_id = athletes.id
        JOIN disciplines
            ON results.discipline_id = disciplines.id
        JOIN competitions
            ON results.competition_id = competitions.id
        ORDER BY results.place, athletes.full_name;
        """
    ).fetchall()

    conn.close()

    return render(
        request,
        "sports/result_list.html",
        {
            "results": results_data,
        },
    )


def result_detail(request, result_id: int):
    """Показать отдельный результат из SQLite."""
    conn = get_connection()

    result = conn.execute(
        """
        SELECT
            results.id,
            athletes.id AS athlete_id,
            athletes.full_name AS athlete_name,
            disciplines.name AS discipline_name,
            competitions.name AS competition_name,
            competitions.date AS competition_date,
            results.result,
            disciplines.unit,
            results.place,
            results.standard,
            CASE
                WHEN results.result <= results.standard
                THEN 1
                ELSE 0
            END AS standard_met
        FROM results
        JOIN athletes
            ON results.athlete_id = athletes.id
        JOIN disciplines
            ON results.discipline_id = disciplines.id
        JOIN competitions
            ON results.competition_id = competitions.id
        WHERE results.id = ?;
        """,
        (result_id,),
    ).fetchone()

    conn.close()

    return render(
        request,
        "sports/result_detail.html",
        {
            "result": result,
        },
        status=404 if result is None else 200,
    )


def athlete_search(request):
    """Найти спортсменов по минимальному году рождения."""
    birth_year = request.GET.get("birth_year")
    athletes_data = []

    if birth_year:
        conn = get_connection()

        athletes_data = conn.execute(
            """
            SELECT
                id,
                full_name,
                birth_year
            FROM athletes
            WHERE birth_year >= ?
            ORDER BY birth_year, full_name;
            """,
            (birth_year,),
        ).fetchall()

        conn.close()

    return render(
        request,
        "sports/athlete_search.html",
        {
            "athletes": athletes_data,
            "birth_year": birth_year,
        },
    )


def statistics(request):
    """Показать статистику результатов по дисциплинам."""
    conn = get_connection()

    statistics_data = conn.execute(
        """
        SELECT
            disciplines.name AS discipline_name,
            disciplines.unit,
            COUNT(results.id) AS results_count,
            MIN(results.result) AS best_result,
            AVG(results.result) AS average_result
        FROM disciplines
        LEFT JOIN results
            ON disciplines.id = results.discipline_id
        GROUP BY
            disciplines.id,
            disciplines.name,
            disciplines.unit
        ORDER BY results_count DESC, disciplines.name;
        """
    ).fetchall()

    conn.close()

    return render(
        request,
        "sports/statistics.html",
        {
            "statistics": statistics_data,
        },
    )
