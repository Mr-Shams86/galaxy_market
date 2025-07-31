from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from products.models.product import Product


def cart_view(request):
    cart = request.session.get('cart', [])
    products = Product.objects.filter(id__in=cart)

    total = sum(p.price for p in products)  # 👈 Считаем сумму

    return render(request, "orders/cart.html", {
        "products": products,
        "total": total  # 👈 Передаём в шаблон
    })


def checkout_view(request):
    return render(request, "orders/checkout.html")


def add_to_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id not in cart:
        cart.append(product_id)
        request.session['cart'] = cart
    return redirect('orders:cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', [])
    if product_id in cart:
        cart.remove(product_id)
        request.session['cart'] = cart
    return redirect('orders:cart')



@login_required
def my_orders_view(request):
    # Заглушка — позже подключишь реальные данные из модели Order
    orders = [
        {"id": 12345, "items": 2, "date": "2025-06-15"},
        {"id": 12346, "items": 1, "date": "2025-06-18"},
    ]
    return render(request, "orders/my_orders.html", {"orders": orders})
