"""URL-маршруты спортивной части проекта."""

from django.urls import path

from . import views

urlpatterns = [
    path(
        "athletes/",
        views.athletes,
        name="athletes",
    ),
    path(
        "athletes/<int:athlete_id>/",
        views.athlete_detail,
        name="athlete_detail",
    ),
    path(
        "results/",
        views.results,
        name="results",
    ),
    path(
        "results/<int:result_id>/",
        views.result_detail,
        name="result_detail",
    ),
    path(
        "competitions/",
        views.competitions,
        name="competitions",
    ),
]
