import json
import os
from store.models import DATABASE
import hashlib
import re


def filtering_category(database: dict,
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False,
                       ):
    """
    Функция фильтрации данных по параметрам.

    :param database: База данных.
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список.
    """
    if category_key is not None:
        result = [value for value in database.values() if value['category'] == category_key]
    else:
        result = [*database.values()]
    if ordering_key is not None:
        result.sort(key=lambda x: x[ordering_key], reverse=reverse)
    return result


def add_user_in_cart(username: str):

    if os.path.exists('cart.json'):  # Если существует
        # Читаем содержимое
        with open('cart.json', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую корзину
            cart = json.load(f)
        if username not in cart:
            # Обновляем содержимое корзины новым пользователем
            cart.update({username: {'products': {}}})
            with open('cart.json', mode='w', encoding='utf-8') as f:  # Записываем корзину
                json.dump(cart, f)
        return None

    cart = {username: {'products': {}}}  # Создаём пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем корзину
        json.dump(cart, f)


def view_in_cart() -> dict:
    """
    Просматривает содержимое cart.json

    :return: Содержимое 'cart.json'
    """
    user = get_user()
    if os.path.exists('cart.json'):  # Если файл существует
        with open('cart.json', encoding='utf-8') as f:
            return json.load(f)

    cart = {user: {'products': {}}}  # Создаём пустую корзину
    with open('cart.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую корзину
        json.dump(cart, f)

    return cart


def add_to_cart(id_product: str) -> bool:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart()  # Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.
    cart = cart_users[get_user()]
    # Проверьте, а существует ли такой товар в корзине, если нет, то перед тем как его добавить - проверьте есть ли такой
    # id товара в вашей базе данных DATABASE, чтобы уберечь себя от добавления несуществующего товара.

    if id_product not in cart['products']:
        if not DATABASE.get(id_product):
            return False
        cart['products'][id_product] = 1
    else:
        cart['products'][id_product] += 1
    # Если товар существует, то увеличиваем его количество на 1

    # Не забываем записать обновленные данные cart в 'cart.json'
    with open('cart.json', mode='w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    return True


def remove_from_cart(id_product: str) -> bool:
    """
    Добавляет позицию продукта из корзины. Если в корзине есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    cart_users = view_in_cart()  # Помните, что у вас есть уже реализация просмотра корзины,
    # поэтому, чтобы загрузить данные из корзины, не нужно заново писать код.
    cart = cart_users[get_user()]
    # Проверьте, а существует ли такой товар в корзине, если нет, то возвращаем False.
    if id_product not in cart['products']:
        return False

    cart['products'].pop(id_product)  # Если существует, то удаляем ключ 'id_product' у cart['products'].

    # Не забываем записать обновленные данные cart в 'cart.json'
    with open('cart.json', mode='w', encoding='utf-8') as f:
        json.dump(cart_users, f)

    return True

def view_in_users() -> dict:
    """
    Просматривает содержимое users.json

    :return: Содержимое 'users.json'
    """
    if os.path.exists('users.json'):  # Если файл существует
        with open('users.json', encoding='utf-8') as f:
            return json.load(f)

    users = {}  # Создаём пустую базу данных пользователей

    with open('users.json', mode='x', encoding='utf-8') as f:   # Создаём файл и записываем туда пустую базу
        json.dump(users, f)

    return users


def check_password(password):
    pattern = r"^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$"
    return bool(re.match(pattern, password))

def check_user_before_add(username: str, email:str, password1: str, password2: str) -> bool:
    """

    :param username:
    :param email:
    :param password1:
    :param password2:
    :return:
    """
    result = {"answer": True, "error": None}
    users = view_in_users()

    if username in users:  # Если пользователь уже есть в базе возвращаем ошибку
        result["answer"] = False
        result["error"] = "Такой username уже занят"
        return result

    # Осуществление поиска по email
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


def check_user(username: str, password: str):
    """
    Проверка пользователя при авторизации
    :param username:
    :param password:
    :return:
    """

    users = view_in_users()
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

def add_to_users(username: str, email:str, password1:str, password2:str,) -> dict:
    """
    Добавляет продукт в корзину. Если в корзине нет данного продукта, то добавляет его с количеством равное 1.
    Если в корзине есть такой продукт, то добавляет количеству данного продукта + 1.

    :param password1:
    :param password2:
    :param email:
    :param username:
    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """

    check = check_user_before_add(username, email, password1, password2)
    if not check["answer"]:
        return check

    # Если пройдены все проверки, то добавляем пользователя
    users = view_in_users()  # Помните, что у вас есть уже реализация просмотра корзины,
    hash_password = hashlib.sha256(password1.encode()).hexdigest()
    users[username] = {"email": email,
                       "password": hash_password}

    # Не забываем записать обновленные данные cart в 'cart.json'
    with open('users.json', mode='w', encoding='utf-8') as f:
        json.dump(users, f)

    return check

def get_user() -> str|None:
    """

    :return:
    """
    if os.path.exists('auth_user.json'):  # Если файл существует
        with open('auth_user.json', encoding='utf-8') as f:
            return json.load(f)["user"]

    user = {"user": ""}  # Создаём пустую базу данных пользователей

    with open('auth_user.json', mode='x', encoding='utf-8') as f:  # Создаём файл и записываем туда пустую базу
        json.dump(user, f)

    return user


def save_auth_user(username) -> None:
    with open('auth_user.json', mode='w',encoding='utf-8') as f:  # Создаём файл и записываем туда пустую базу
        json.dump({"user": username}, f)

def authenticate(username: str):
    user = get_user()
    if username != user:
        save_auth_user(username)
    add_user_in_cart(username)

def logout():
    save_auth_user("")


def show_user(view_func):
    def wrapper(request, *args, **kwargs):
        request.user.username = get_user()
        return view_func(request, *args, **kwargs)
    return wrapper


from django.shortcuts import redirect

def authentication_required(url):
    def login(view_func):
        def wrapper(request, *args, **kwargs):
            if get_user():
                # Пользователь авторизован, выполняем представление
                return view_func(request, *args, **kwargs)
            else:
                # Пользователь не авторизован, перенаправляем его на страницу входа
                return redirect(url)

        return wrapper
    return login



if __name__ == "__main__":
    # Проверка работоспособности функций view_in_cart, add_to_cart, remove_from_cart
    print(view_in_cart())  # {'products': {}}
    print(add_to_cart('1'))  # True
    print(add_to_cart('0'))  # False
    print(add_to_cart('1'))  # True
    print(add_to_cart('2'))  # True
    print(view_in_cart())  # {'products': {'1': 2, '2': 1}}
    print(remove_from_cart('0'))  # False
    print(remove_from_cart('1'))  # True
    print(view_in_cart())  # {'products': {'2': 1}}

    # from store.models import DATABASE
    #
    # test = [
    #     {'name': 'Клубника', 'discount': None, 'price_before': 500.0, 'price_after': 500.0,
    #      'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
    #      'category': 'Фрукты', 'id': 2, 'url': 'store/images/product-2.jpg', 'html': 'strawberry'
    #      },
    #
    #     {'name': 'Яблоки', 'discount': None, 'price_before': 130.0, 'price_after': 130.0,
    #      'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
    #      'category': 'Фрукты', 'id': 10, 'url': 'store/images/product-10.jpg', 'html': 'apple'
    #      }
    # ]
    #
    # print(filtering_category(DATABASE, 'Фрукты', 'price_after', True) == test)  # True
