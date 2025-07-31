from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from products.models.product import Product

def cart_view(request):
    cart = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart.keys())

    items = []
    total = 0

    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal
        items.append({
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        })

    return render(request, "orders/cart.html", {
        "items": items,
        "total": total,
    })


def checkout_view(request):
    return render(request, "orders/checkout.html")


def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('orders:cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('orders:cart')


def add_quantity(request, product_id):
    return add_to_cart(request, product_id)


def remove_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('orders:cart')


@login_required
def my_orders_view(request):
    # Заглушка — позже подключишь реальные данные из модели Order
    orders = [
        {"id": 12345, "items": 2, "date": "2025-06-15"},
        {"id": 12346, "items": 1, "date": "2025-06-18"},
    ]
    return render(request, "orders/my_orders.html", {"orders": orders})
