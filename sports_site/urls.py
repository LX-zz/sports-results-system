"""Основная маршрутизация Django-проекта."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("", include("sports.urls")),
]

handler404 = "homepage.views.page_not_found"
