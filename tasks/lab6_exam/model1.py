from datetime import time, timedelta

DATABASE = [{"event": "Поход в театр",  "start_time": time(10, 0), "duration": timedelta(minutes=60)},
            {"event": "Поход в театр1",  "start_time": time(12, 0), "duration": timedelta(minutes=60)},
            {"event": "Поход в театр2",  "start_time": time(14, 0), "duration": timedelta(minutes=60)},
            ]


def add_event(event_time: time, event_name: str, event_duration: timedelta) -> time:
    """
    Добавляет событие в список событий в отсортированном порядке с учетом временных ограничений.
    :param event_time: время начала события
    :param event_name: имя события
    :param event_duration: продолжительность события
    :return: время начала события после добавления
    """
    # Ограничение времени с 8:00 до 20:00
    start_limit = time(8, 0)
    end_limit = time(20, 0)
    current_time = event_time

    # Если событие начинается раньше 8:00, переносим его на 8:00
    if event_time < start_limit:
        current_time = start_limit

    # Если событие оканчивается позже 20:00, переносим его на 20:00 минус продолжительность события
    if current_time + event_duration > end_limit:
        return None

    # Ищем место для вставки события в список
    for i, entry in enumerate(DATABASE):
        if current_time + event_duration <= entry["start_time"]:
            DATABASE.insert(i, {"event": event_name, "start_time": current_time, "duration": event_duration})
            return current_time
        current_time = entry["start_time"] + entry["duration"]

    # Если не нашли подходящего места, добавляем событие в конец
    # DATABASE.append({"event": event_name, "start_time": current_time, "duration": event_duration})

    return current_time


print(add_event(time(10, 00), "1", timedelta(minutes=60)), DATABASE)
print(add_event(datetime(2023, 10, 16), "2"), DATABASE)
print(add_event(datetime(2023, 10, 15), "2"), DATABASE)