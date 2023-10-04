from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from .models import DATABASE


def products_view(request):
    if request.method == "GET":
        if id_product := request.GET.get("id"):
            if data := DATABASE.get(id_product):
                return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})


def products_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):
            for data in DATABASE.values():
                if data['html'] == page:
                    with open(f'store/products/{page}.html', encoding="utf-8") as f:
                        data = f.read()  # Читаем HTML файл
                    return HttpResponse(data)  # Отправляем HTML файл как ответ
        elif isinstance(page, int):
            # Обрабатываем условие того, что пытаемся получить страницу товара по его id
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:
                with open(f'store/products/{data["html"]}.html', encoding="utf-8") as f:
                    data = f.read()
                return HttpResponse(data)

        return HttpResponse(status=404)


def shop_view(request):
    if request.method == "GET":
        with open('store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ


def coupon_check_view(request, data):
    if request.method == "GET":
        if data == "coupon":
            return JsonResponse({"discount": 10, "is_valid": True})
        return HttpResponseNotFound("Неверный купон")


def delivery_estimate_view(request):
    if request.method == "GET":
        data = request.GET
        if data.get('country').lower() != 'россия':
            return HttpResponseNotFound("Неверные данные")
        return JsonResponse({"price": 100.00})


def cart_view(request):
    if request.method == "GET":
        with open('store/cart.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ
