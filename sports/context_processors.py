"""Общие данные для шаблонов Sports Results."""

from .models import Athlete, Competition


def site_info(request):
    """Передать общую информацию во все шаблоны."""
    return {
        "site_name": "Sports Results",
        "total_athletes": Athlete.objects.count(),
        "total_competitions": Competition.objects.count(),
    }
