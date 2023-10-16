from datetime import datetime, timedelta

DATABASE = [{"date": datetime(2023, 10, 16), "event": "Поход в театр"},
            {"date": datetime(2023, 10, 17), "event": "Встреча с коллегой"},
            {"date": datetime(2023, 10, 19), "event": "Поход в кино"},
            ]


def add_event(event_date: datetime, event_name: str) -> datetime:
    """
    Добавляет событие в список событий в отсортированном порядке
    :param event_date: дата добавляемого события
    :param event_name: имя события
    :return: дату когда в итоге добавили событие
    """
    for i, entry in enumerate(DATABASE):  # Перебор по всем датам календаря
        if event_date < entry["date"]:  # Ищем когда дата нового события будет явно меньше даты в текущем индексе
            DATABASE.insert(i, {"date": event_date, "event": event_name})  # Добавляем в календарь это событие
            return event_date  # Возвращаем дату на которое записали событие
        event_date += timedelta(days=1)  # Иначе переносим событие на следующий день
    DATABASE.append({"date": event_date, "event": event_name})  # Если не нашли место до добавляем в конец последней записи календаря
    return event_date

