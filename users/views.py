import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model, logout

from .forms import CustomUserCreationForm, ProfileForm

logger = logging.getLogger(__name__)
User = get_user_model()  # Используем кастомную модель пользователя


# ✅ Регистрация нового пользователя
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            logger.info(f"Новый пользователь зарегистрирован: {user.email}")
            messages.success(request, "Регистрация прошла успешно! Можете войти.")
            return redirect("users:login")
        else:
            logger.warning("❌ Ошибка при регистрации: некорректные данные")
            messages.error(request, "Ошибка при регистрации. Проверьте данные.")
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})


# ✅ Просмотр / создание профиля
@login_required
def profile(request):
    user = request.user
    if not hasattr(user, "profile"):
        # Профиль ещё не создан — создаём при отправке POST
        if request.method == "POST":
            ProfileForm(user=user).save()
            messages.success(request, "Профиль создан.")
            return redirect("users:profile")
        return render(request, "users/profile.html", {"user": user})

    return render(request, "users/profile.html", {"user": user})


# ✅ Редактирование профиля
@login_required
def edit_profile(request):
    profile = request.user.profile
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            logger.info(f"Профиль пользователя {request.user.email} обновлён.")
            messages.success(request, "Профиль успешно обновлён.")
            return redirect("users:profile")
    else:
        form = ProfileForm(instance=profile)
    return render(request, "users/edit_profile.html", {"form": form})


# ✅ Удаление профиля
@login_required
def delete_profile(request):
    if request.method == "POST":
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Профиль удалён.")
        return redirect("products:index")  # или на 'home'
    return render(request, "users/delete_confirm.html")


# ✅ Публичный просмотр профиля пользователя
def view_profile(request, user_id):
    target_user = get_object_or_404(User, pk=user_id)
    return render(
        request,
        "users/view_profile.html",
        {
            "user": target_user,
            "profile": target_user.profile,
        },
    )



# ✅ Публичный профиль продавца
def seller_profile(request, user_id):
    seller = get_object_or_404(User, pk=user_id)
    return render(
        request,
        "users/sellerprofile.html",
        {
            "seller": seller,
            "profile": seller.profile,
        },
    )


# ✅ Подтверждение выхода из аккаунта
@login_required
def logout_confirm(request):
    if request.method == "POST":
        logout(request)
        messages.info(request, "Вы вышли из аккаунта.")
        return redirect("products:index")
    return render(request, "users/logout_confirm.html")
