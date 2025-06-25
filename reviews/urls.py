from django.urls import path
from .views import my_reviews_view

app_name = "reviews"

urlpatterns = [
    path("my/", my_reviews_view, name="my_reviews"),
]
