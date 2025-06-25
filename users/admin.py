from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Profile


# Сначала описываем Inline для профиля
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = "Профиль"
    fk_name = "user"
    readonly_fields = ("avatar_tag",)

    def avatar_tag(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%;" />',
                obj.avatar.url,
            )
        return "-"

    avatar_tag.short_description = "Avatar"


# Теперь регистрируем кастомного пользователя с этим Inline
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    inlines = [ProfileInline]

    list_display = ("id", "email", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser")
    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


# Админка отдельно для профиля, если нужно
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "nickname", "avatar_tag", "bio", "created_at")
    search_fields = ("user__username", "nickname", "bio")
    list_filter = ("created_at",)
    readonly_fields = ("avatar_tag",)

    def avatar_tag(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:50%;" />',
                obj.avatar.url,
            )
        return "-"

    avatar_tag.short_description = "Avatar"
