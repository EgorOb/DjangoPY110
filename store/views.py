from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from .models import DATABASE


def products_view(request):
    if request.method == "GET":
        if id_product := request.GET.get("id"):
            if data := DATABASE.get(id_product):
                return JsonResponse(data)
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        return JsonResponse(DATABASE)
