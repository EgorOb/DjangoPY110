from datetime import datetime, timedelta

# Обновленная база данных с учетом возможного добавления нового пользователя
DATABASE = [{"user": "user", "date": datetime(2023, 10, 16), "event": "Поход в театр"},
            {"user": "user", "date": datetime(2023, 10, 17), "event": "Встреча с коллегой"},
            {"user": "user", "date": datetime(2023, 10, 19), "event": "Поход в кино"},
            ]


def add_event(event_date: datetime, event_name: str, user: str) -> datetime:
    """
    Добавляет событие в список событий в отсортированном порядке с учетом пользователя.
    :param event_date: дата добавляемого события
    :param event_name: имя события
    :param user: имя пользователя
    :return: дату когда в итоге добавили событие
    """

    # TODO Если пользователя нет в БД, создаем запись с его исходными данными {"user": ..., "date": ..., "event": ...}

    for i, entry in enumerate(DATABASE):  # Перебор по всем датам календаря
        if event_date < entry["date"]:  # TODO Помнить что теперь есть еще условие про прользователя
            DATABASE.insert(i, {"date": event_date, "event": event_name})  # TODO Добавить "user" в словарь
            return event_date
        event_date += timedelta(days=1)  # TODO Доработать код, для обработки пользователя. Помним смещение события может быть только
    #  в строках относящихся к причастному пользователю

    DATABASE.append({"date": event_date, "event": event_name})  # TODO Добавить "user" в словарь
    return event_date