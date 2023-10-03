# urls.py in store

from django.urls import path
from .views import products_view, shop_view, cart_view, coupon_check_view, delivery_estimate_view

urlpatterns = [
    path('product/', products_view),
    path('', shop_view),
    path('cart/', cart_view),
    path('coupon/check/<slug:data>', coupon_check_view),
    path('delivery/estimate/', delivery_estimate_view),
]