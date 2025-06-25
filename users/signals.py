import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, "profile"):
        base_nickname = f"User{instance.id}"
        nickname = base_nickname
        counter = 1

        # Проверка уникального ника
        while Profile.objects.filter(nickname=nickname).exists():
            nickname = f"{base_nickname}_{counter}"
            counter += 1

        # Создание профиля
        profile = Profile(user=instance, nickname=nickname)
        profile.full_clean()  # вызовет clean() с проверками
        profile.save()

        # Лог
        print(f"Профиль пользователя {instance.email} успешно создан.")

    # Лог
    print(f"Профиль пользователя {instance.email} обновлен.")
