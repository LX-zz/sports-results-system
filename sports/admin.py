"""Административная панель Sports Results."""

from django.contrib import admin

from .models import Athlete, Competition, Discipline, Result


class ResultInline(admin.TabularInline):
    model = Result
    extra = 0
    show_change_link = True
    fields = (
        "discipline",
        "competition",
        "result",
        "place",
        "standard",
    )


@admin.register(Athlete)
class AthleteAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "birth_year",
    )
    list_display_links = ("id", "full_name")
    search_fields = ("full_name",)
    list_filter = ("birth_year",)
    ordering = ("full_name",)
    list_per_page = 20
    inlines = [ResultInline]


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "unit",
    )
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "date",
    )
    search_fields = ("name",)
    list_filter = ("date",)
    ordering = ("-date",)
    date_hierarchy = "date"


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "athlete",
        "discipline",
        "competition",
        "result",
        "place",
        "standard_status",
    )
    search_fields = (
        "athlete__full_name",
        "discipline__name",
        "competition__name",
    )
    list_filter = (
        "discipline",
        "competition",
        "place",
    )
    ordering = ("place", "id")
    list_select_related = (
        "athlete",
        "discipline",
        "competition",
    )
    autocomplete_fields = (
        "athlete",
        "discipline",
        "competition",
    )

    @admin.display(
        description="Норматив выполнен",
        boolean=True,
    )
    def standard_status(self, obj):
        return obj.check_standard()
