from django.urls import path
from .views import products_view


urlpatterns = [
   path('product/', products_view),
]
