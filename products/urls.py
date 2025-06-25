from django.urls import path
from products.views import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    PaymentSuccessView,
    PaymentFailedView,
    create_checkout_session,
)

app_name = "products"

urlpatterns = [
    path("", ProductListView.as_view(), name="index"),
    path("<int:pk>/", ProductDetailView.as_view(), name="detail"),
    path("additem/", ProductCreateView.as_view(), name="add_item"),
    path("updateitem/<int:pk>/", ProductUpdateView.as_view(), name="update_item"),
    path("deleteitem/<int:pk>/", ProductDeleteView.as_view(), name="delete_item"),
    path("success/", PaymentSuccessView.as_view(), name="success"),
    path("failed/", PaymentFailedView.as_view(), name="failed"),
    path(
        "api/checkout-session/<int:id>/",
        create_checkout_session,
        name="api_checkout_session",
    ),
]
