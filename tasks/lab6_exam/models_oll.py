from datetime import datetime, timedelta, time

DATABASE = [{"date": datetime(2023, 10, 16),
             "events": [
                 {"event": "Встреча с коллегой",
                  "start_time": time(10, 0),
                  "duration": timedelta(minutes=60)},

                 {"event": "Обед",
                  "start_time": time(13, 0),
                  "duration": timedelta(minutes=60)},
             ]},
            {"date": datetime(2023, 10, 17),
             "events": [
                 {"event": "Презентация",
                  "start_time": time(14, 30),
                  "duration": timedelta(minutes=45)},

                 {"event": "Поход в кино",
                  "start_time": time(17, 30),
                  "duration": timedelta(minutes=120)}
             ]},
            ]


def add_event(event_date: datetime, event_name: str, start_time: time, duration: int) -> datetime:
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
    DATABASE.append({"date": event_date,
                     "event": event_name})  # Если не нашли место до добавляем в конец последней записи календаря
    return event_date


print(add_event(datetime(2023, 10, 16), "1", time(8, 0), 60), DATABASE)
print(add_event(datetime(2023, 10, 16), "2"), DATABASE)
print(add_event(datetime(2023, 10, 15), "2"), DATABASE)
