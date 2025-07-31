from django.urls import path
from .views import (
    cart_view,
    checkout_view,
    my_orders_view,
    add_quantity,
    add_to_cart,
    remove_quantity,
    remove_from_cart,
    success_view,
)

app_name = "orders"

urlpatterns = [
    path("cart/", cart_view, name="cart"),
    path("add/<int:product_id>/", add_to_cart, name="add_to_cart"),  # ✅ добавление
    path("increase/<int:product_id>/", add_quantity, name="add_quantity"),  # ➕ увеличить
    path("remove_one/<int:product_id>/", remove_quantity, name="remove_quantity"),  # ➖ уменьшить
    path("delete/<int:product_id>/", remove_from_cart, name="remove_from_cart"),  # ❌ удалить
    path("checkout/", checkout_view, name="checkout"),
    path("success/", success_view, name="success"),
    path("my/", my_orders_view, name="my_orders"),
]
