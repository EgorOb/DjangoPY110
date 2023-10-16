from django.http import HttpResponse, HttpRequest
from datetime import datetime
from django.views import View
from .models import add_event


class DateView(View):

    def get(self, request: HttpRequest, user: str, event: str, dt: datetime) -> HttpResponse:
        date = add_event(dt, event, user).strftime('%Y-%m-%d')  # Приведем наш datetime к виду YYYY-MM-DD для вывода
        return HttpResponse(f"Событие {event} добавлено в календарь для {user} на дату: {date}")
