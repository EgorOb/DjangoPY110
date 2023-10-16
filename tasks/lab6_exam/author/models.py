from datetime import datetime, timedelta


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
    user_exists = any(entry["user"] == user for entry in DATABASE)

    if not user_exists:
        # Если пользователя нет в БД, создаем запись с его исходными данными
        DATABASE.append({"user": user, "date": event_date, "event": event_name})
        return event_date

    for i, entry in enumerate(DATABASE):
        if event_date < entry["date"] and user == entry["user"]:
            # Ищем когда дата нового события будет явно меньше даты в текущем индексе
            DATABASE.insert(i, {"user": user, "date": event_date, "event": event_name})
            return event_date
        if user == entry["user"]:
            event_date += timedelta(days=1)

    DATABASE.append({"user": user, "date": event_date, "event": event_name})
    return event_date

# print(add_event(datetime(2023, 10, 16), "1", user="user"), DATABASE)
# print(add_event(datetime(2023, 10, 16), "2", user="user"), DATABASE)
# print(add_event(datetime(2023, 10, 16), "2", user="user1"), DATABASE)
# print(add_event(datetime(2023, 10, 16), "3", user="user1"), DATABASE)
# print(add_event(datetime(2023, 10, 16), "3", user="user1"), DATABASE)
# print(add_event(datetime(2023, 10, 15), "3", user="user1"), DATABASE)