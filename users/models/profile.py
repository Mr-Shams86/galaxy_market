import re
from django.db import models
from django.core.validators import RegexValidator
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from django.core.files.storage import default_storage
from django.templatetags.static import static

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
    
    # 🔒 Безопасный URL аватара: если файла нет — отдаём дефолт из static
    @property
    def avatar_safe_url(self) -> str:
        if self.avatar and default_storage.exists(self.avatar.name):
            return self.avatar.url
        return static("img/default/default-avatar.png")

    def avatar_tag(self):
        # Используем безопасный URL, чтобы админка не падала на битых ссылках
        return format_html(
            '<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:6px;" />',
            self.avatar_safe_url,
        )

    avatar_tag.short_description = "Аватар"

    def clean(self):
        # ✔️ ник может быть пустым — учитываем это
        if self.nickname:
            if self.nickname.lower() == "admin":
                raise ValidationError("Ник 'admin' запрещён.")
            if not re.match(r"^[a-zA-Z0-9_]+$", self.nickname):
                raise ValidationError(
                    "Ник может содержать только латиницу, цифры и подчёркивания."
                )

        if self.avatar and self.avatar.size > 2 * 1024 * 1024:
            raise ValidationError("Аватар не должен превышать 2MB.")

        if self.bio and len(self.bio) > 500:
            raise ValidationError("Описание не должно превышать 500 символов.")

