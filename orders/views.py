from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from products.models.product import Product

from .forms import CheckoutForm

from .models import Order, OrderItem


@login_required
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

    total_quantity = sum(item['quantity'] for item in items)
    
    return render(request, "orders/cart.html", {
        "items": items,
        "total": total,
        "total_quantity": total_quantity,
    })

@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('orders:cart')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            products = Product.objects.filter(id__in=cart.keys())
            
            total = 0
            for product in products:
                quantity = cart.get(str(product.id), 0)
                total += product.price * quantity

            # Сохраняем заказ
            order = Order.objects.create(
                user=request.user,
                name=form.cleaned_data['name'],
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
                total_price=total
            )

            # Сохраняем позиции заказа
            for product in products:
                quantity = cart.get(str(product.id), 0)
                if quantity > 0:
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=quantity,
                        price=product.price,
                    )

            # Очищаем корзину
            request.session['cart'] = {}
            request.session.modified = True

            return redirect('orders:success')
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form})


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('orders:cart')


@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)
    if product_id_str in cart:
        del cart[product_id_str]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('orders:cart')


@login_required
def add_quantity(request, product_id):
    return add_to_cart(request, product_id)


@login_required
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
    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related("items__product")
        .order_by('-created_at')
    )
    
    orders_data = []    
    for order in orders:
        items_with_subtotal = []
        total_quantity = 0
        total_price = 0

        for item in order.items.all():
            subtotal = item.price * item.quantity
            total_quantity += item.quantity
            total_price += subtotal
            items_with_subtotal.append({
                "product": item.product,
                "price": item.price,
                "quantity": item.quantity,
                "subtotal": subtotal,
            })

        orders_data.append({
            "order": order,
            "items": items_with_subtotal,
            "total_quantity": total_quantity,
            "total_price": total_price,
        })

    return render(request, "orders/my_orders.html", {
        "orders": orders_data,
        "message": "У вас нет заказов." if not orders_data else None
    })




@login_required
def success_view(request):
    latest_order = (
        Order.objects
        .filter(user=request.user)
        .order_by('-created_at')
        .prefetch_related("items__product")
        .first()
    )

    if not latest_order:
        return redirect('products:index')

    # Собираем данные с подсчётом total_quantity и subtotal по каждому товару
    items_with_subtotal = []
    total_quantity = 0

    for item in latest_order.items.all():
        subtotal = item.price * item.quantity
        total_quantity += item.quantity
        items_with_subtotal.append({
            "product": item.product,
            "price": item.price,
            "quantity": item.quantity,
            "subtotal": subtotal,
        })

    return render(request, 'payment_success.html', {
        'order': latest_order,
        'total_quantity': total_quantity,
        'items': items_with_subtotal,  # ✅ список с подсчитанными total'ами
    })

