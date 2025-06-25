from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def cart_view(request):
    return render(request, "orders/cart.html")


def checkout_view(request):
    return render(request, "orders/checkout.html")


@login_required
def my_orders_view(request):
    # Заглушка — позже подключишь реальные данные из модели Order
    orders = [
        {"id": 12345, "items": 2, "date": "2025-06-15"},
        {"id": 12346, "items": 1, "date": "2025-06-18"},
    ]
    return render(request, "orders/my_orders.html", {"orders": orders})
