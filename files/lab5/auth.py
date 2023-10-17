import os
import re
import json
import hashlib


def get_all_users() -> dict:
    """
    Просматривает содержимое users.json
    Если базы не существует, то создаётся users.json

    :return: Содержимое 'users.json'
    """
    if os.path.exists('users.json'):  # Если файл существует, то возвращаем содержимое файла
        with open('users.json', encoding='utf-8') as f:
            return json.load(f)

    users = {}  # Создаём пустую базу данных пользователей

    with open('users.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую базу
        json.dump(users, f)

    return users


def check_password(password: str) -> bool:
    """
    Проверка пароля по его паттерну регулярного выражения на достаточную сложность
    Минимум 8 символов, минимум 1 заглавная буква, минимум 1 цифра, минимум 1 спец символ из списка [!@#$%^&*]
    :param password: Пароль
    :return: Возвращает True, если
    """
    pattern = r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$"
    return bool(re.match(pattern, password))


def check_user_before_registration(username: str, email: str, password1: str, password2: str) -> dict:
    """
    Проверяет данные пользователя при регистрации. Возвращает словарь
    {"answer": bool, "error": str}, где:
        answer - булево значение сообщающее о всех пройденных проверках;
        error - текст ошибки в случае ошибок на проверках

    :param username: Логин пользователя
    :param email: Email пользователя
    :param password1: Пароль из первой строки
    :param password2: Пароль из второй строки
    :return: {"answer": bool, "error": str}
    """
    result = {"answer": True, "error": None}
    users = get_all_users()

    # Проверка на существование username в базе данных
    if username in users:
        result["answer"] = False
        result["error"] = "Такой username уже занят"
        return result

    # Проверка на существование email в базе данных
    for user in users.values():
        if user["email"] == email:
            result["answer"] = False
            result["error"] = "Пользователь с таким email уже зарегистрирован"
            return result

    # Проверка требования пароля
    if not check_password(password1):
        result["answer"] = False
        result["error"] = "Пароль не проходит критериям безопасности: " \
                          "минимум 8 символов; минимум 1 заглавная буква; " \
                          "минимум 1 цифра; минимум 1 специальный символ из списка [!@#$%^&*]"
        return result

    # Проверка совпадения паролей
    if not (password1 == password2):
        result["answer"] = False
        result["error"] = "Пароли не совпадают"
        return result
    return result


def check_user_before_authorization(username: str, password: str) -> dict:
    """
    Проверка пользователя перед авторизацией
    :param username: Логин пользователя
    :param password: Пароль пользователя
    :return: {"answer": bool, "error": str}
    """

    users = get_all_users()
    result = {"answer": True, "error": None}

    if username not in users:  # Проверка, что пользователь есть в базе данных
        result["answer"] = False
        result["error"] = "Такого username не существует"
        return result

    # Проверка, что пароли совпадают
    hash_password = hashlib.sha256(password.encode()).hexdigest()
    if not (users[username]["password"] == hash_password):
        result["answer"] = False
        result["error"] = "Пароль введён неверно"
        return result

    return result


def add_to_users_database(username: str, email: str, password: str) -> None:
    """
    Добавляет пользователя в базу данных. Считается, что данные пользователя валидны

    :param username: Логин пользователя
    :param email: Email пользователя
    :param password: Пароль пользователя
    """

    users = get_all_users()  # Загружаем данные из БД
    hash_password = hashlib.sha256(password.encode()).hexdigest()  # Трансформируем пароль
    users[username] = {"email": email,
                       "password": hash_password}

    # Записываем данные в БД 'users.json'
    with open('users.json', mode='w', encoding='utf-8') as f:
        json.dump(users, f)


def get_current_auth_user() -> str:
    """
    Получение имени пользователя, который сейчас авторизирован в системе
    :return: Имя пользователя в системе
    """
    if os.path.exists('auth_user.json'):  # Если файл существует
        with open('auth_user.json', encoding='utf-8') as f:
            return json.load(f)["user"]

    user = {"user": ""}  # Создаём заглушку для не авторизированного пользователя

    with open('auth_user.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую базу
        json.dump(user, f)

    return user["user"]


def set_current_auth_user(username) -> None:
    """
    Установить пользователя как авторизированного
    :param username: Имя пользователя
    :return: None
    """
    with open('auth_user.json', mode='w', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую базу
        json.dump({"user": username}, f)


def authenticate(username: str) -> None:
    """
    Функция проводит процедуру авторизации в системе

    :param username: Имя пользователя
    :return: None
    """
    user = get_current_auth_user()
    if username != user:
        set_current_auth_user(username)


def logout():
    """
    Выход пользователя из системы

    :return: None
    """
    set_current_auth_user("")
