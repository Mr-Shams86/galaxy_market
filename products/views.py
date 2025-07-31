import json
import stripe
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from products.mixins import SellerRequiredMixin
from .models import Product


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "items"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["show_add_button"] = (
            self.request.user.is_authenticated and self.request.user.profile.is_seller
        )
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/detail.html"
    context_object_name = "item"
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stripe_publishable_key"] = settings.STRIPE_PUBLISHABLE_KEY
        return context


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = "products/additem.html"
    fields = ["name", "price", "description", "category", "image"]
    success_url = reverse_lazy("products:index")

    def form_valid(self, form):
        form.instance.seller = self.request.user
        form.instance.category = form.cleaned_data["category"]
        messages.success(self.request, "Товар успешно добавлен!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "⚠️ Ошибка при добавлении товара. Проверьте данные."
        )
        return super().form_invalid(form)


class ProductUpdateView(LoginRequiredMixin, SellerRequiredMixin, UpdateView):
    model = Product
    template_name = "products/updateitem.html"
    pk_url_kwarg = "pk"
    fields = ["name", "price", "description", "image"]
    success_url = reverse_lazy("products:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item'] = self.get_object()
        return context

    def form_valid(self, form):
        image = self.request.FILES.get("image")
        if image:
            form.instance.image = image
        messages.success(self.request, "Товар успешно обновлён!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Ошибка при обновлении товара.")
        return super().form_invalid(form)


class ProductDeleteView(LoginRequiredMixin, SellerRequiredMixin, DeleteView):
    model = Product
    template_name = "products/deleteitem.html"
    pk_url_kwarg = "pk"
    success_url = reverse_lazy("products:index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["item"] = self.get_object()
        return context

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, f"Товар «{obj.name}» успешно удалён!")
        return super().delete(request, *args, **kwargs)



@login_required
@require_POST
@csrf_protect
def create_checkout_session(request, id):
    product = get_object_or_404(Product, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=request.user.email,
        payment_method_types=["card"],
        line_items=[
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": product.name},
                    "unit_amount": int(product.price * 100),
                },
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=request.build_absolute_uri(reverse("products:success"))
        + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=request.build_absolute_uri(reverse("products:failed")),
    )

    print("CHECKOUT SESSION:", checkout_session)

    OrderDetail.objects.create(
        customer_username=request.user.email,
        product=product,
        stripe_payment_intent=checkout_session["id"],
        amount=product.price,
    )

    return JsonResponse({"sessionId": checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "payment_success.html"

    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")
        if not session_id:
            return HttpResponseNotFound()

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.retrieve(session_id)

        order = get_object_or_404(OrderDetail, stripe_payment_intent=session.id)
        order.has_paid = True
        order.save()
        return render(request, self.template_name)


class PaymentFailedView(TemplateView):
    template_name = "payment_failed.html"
