import re
from django.db import models
from django.core.validators import RegexValidator
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Пользователь",
    )

    nickname = models.CharField(
        max_length=50,
        unique=True,
        blank=True,
        null=True,
        verbose_name="Никнейм",
        help_text="Придумайте уникальный никнейм",
    )

    bio = models.TextField(blank=True, verbose_name="О себе")

    avatar = models.ImageField(
        upload_to="profile_images/", blank=True, null=True, verbose_name="Аватар"
    )

    contact_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                r"^\+998\d{9}$", message="Введите номер в формате +998xxxxxxxxx"
            )
        ],
        verbose_name="Номер телефона",
    )

    is_seller = models.BooleanField(default=False, verbose_name="Продавец")

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата регистрации"
    )

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"

    def __str__(self):
        return f"Профиль пользователя {self.user.email}"

    def avatar_tag(self):
        if self.avatar:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:6px;" />',
                self.avatar.url,
            )
        return "-"

    avatar_tag.short_description = "Аватар"

    def clean(self):
        # Ограничение: Ник не может быть "admin"
        if self.nickname.lower() == "admin":
            raise ValidationError("Ник 'admin' запрещён.")

        # Ограничение: Только латиница, цифры, подчёркивания
        if not re.match(r"^[a-zA-Z0-9_]+$", self.nickname):
            raise ValidationError(
                "Ник может содержать только латиницу, цифры и подчёркивания."
            )

        # Проверка био и аватара (у тебя уже есть)
        if self.avatar and self.avatar.size > 2 * 1024 * 1024:
            raise ValidationError("Аватар не должен превышать 2MB.")

        if self.bio and len(self.bio) > 500:
            raise ValidationError("Описание не должно превышать 500 символов.")
