from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

app_name = "users"

urlpatterns = [
    # Аутентификация
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/confirm/", views.logout_confirm, name="logout_confirm"),
    path(
        "logout/", LogoutView.as_view(template_name="users/logout.html"), name="logout"
    ),
    # Профиль пользователя
    path("profile/", views.profile, name="profile"),
    path("profile/edit/", views.edit_profile, name="edit_profile"),
    path("profile/delete/", views.delete_profile, name="delete_profile"),
    path("profile/<int:user_id>/", views.view_profile, name="view_profile"),
    # Профиль продавца
    path("seller/<int:user_id>/", views.seller_profile, name="sellerprofile"),
]
