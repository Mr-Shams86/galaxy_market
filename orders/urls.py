from django.urls import path
from .views import cart_view, checkout_view, my_orders_view

app_name = "orders"

urlpatterns = [
    path("cart/", cart_view, name="cart"),
    path("checkout/", checkout_view, name="checkout"),
    path("my/", my_orders_view, name="my_orders"),
]
