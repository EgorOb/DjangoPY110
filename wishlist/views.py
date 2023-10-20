from django.shortcuts import render
from logic.services import view_in_wishlist
from store.models import DATABASE


def wishlist_view(request):
    if request.method == "GET":
        data = view_in_wishlist()[request.user.username]

        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE.get(product_id)
            products.append(product)

        return render(request, 'wishlist/wishlist.html', context={"products": products})
