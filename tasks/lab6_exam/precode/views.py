from django.http import HttpResponse, HttpRequest
from datetime import datetime
from django.views import View
# TODO импортируйте функцию add_event


class DateView(View):

    def get(self, request: HttpRequest, event: str, dt: datetime) -> HttpResponse: # TODO метод должен дополнительно принимать username
        date = ...  # TODO примените функцию add_event и преобразуйте к строковому представлению вида YYYY-MM-DD
        return HttpResponse(f"Событие {event} добавлено в календарь для {...} на дату: {date}") # TODO передайте имя пользователя
