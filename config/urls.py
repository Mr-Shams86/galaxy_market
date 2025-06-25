from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("orders/", include("orders.urls", namespace="orders")),
    path("reviews/", include("reviews.urls", namespace="reviews")),
    path("products/", include("products.urls", namespace="products")),
    path("users/", include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
