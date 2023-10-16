from datetime import datetime


class DateConverter:
    """ Пользовательский конвертер маршрутов. """
    regex = r"\d{4}/\d{2}/\d{2}"  # Регулярное выражение для формата YYYY/MM/DD
    date_format = '%Y/%m/%d'  # Формат вывода для strptime

    def to_python(self, value: str):
        """ Метод преобразует value, полученный после работы регулярного выражения в python тип. """
        return datetime.strptime(value, self.date_format)

    def to_url(self, value: datetime):
        """ Метод обрабатывает python тип, и возвращает строку, которая будет подставлена в url. """
        return value.strftime(self.date_format)
