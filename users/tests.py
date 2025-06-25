from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile
from django.core.exceptions import ValidationError


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", email="testuser@mail.com"
        )

    def test_profile_is_created(self):
        """Профиль должен автоматически создаваться при создании пользователя"""
        self.assertTrue(
            Profile.objects.filter(user=self.user).exists(),
            "❌ Профиль не был создан автоматически",
        )


def test_valid_phone_number(self):
    profile = self.user.profile
    profile.contact_number = "+998901234567"
    try:
        profile.full_clean()  # не должно выбросить ошибку
    except ValidationError:
        self.fail("Правильный номер вызвал ошибку валидации")


def test_invalid_phone_number(self):
    """Телефон с неправильным форматом должен вызвать ошибку"""
    profile = self.user.profile
    profile.contact_number = "12345"  # ❌ неправильный формат
    with self.assertRaises(ValidationError):
        profile.full_clean()  # ✅ вручную проверим валидацию

    # Проверка полей по умолчанию
    self.assertIsNone(profile.avatar, "❌ Аватар по умолчанию должен быть пустым")
    self.assertEqual(
        profile.contact_number,
        "+998909401210",
        "❌ Телефон не соответствует значению по умолчанию",
    )
    self.assertEqual(profile.bio, "")

    # Проверка связанных данных
    self.assertEqual(profile.user.username, "testuser")
    self.assertEqual(profile.user.email, "testuser@mail.com")
    self.assertEqual(str(profile), "Profile of testuser")

    # Упрощённая проверка даты создания
    self.assertEqual(
        profile.created_at.date(),
        self.user.date_joined.date(),
        "❌ Даты создания профиля и пользователя не совпадают",
    )
