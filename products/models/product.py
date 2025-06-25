import os
from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


# Функция для автоматического пути загрузки
def get_upload_path(instance, filename):
    category = (instance.category or "uncategorized").lower().replace(" ", "_")
    name, ext = os.path.splitext(filename)
    filename = f"{instance.name.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}{ext}"
    return f"images/catalog/{category}/{filename}"


# Категории товара (адаптировано под запчасти)
CATEGORY_CHOICES = [
    ("phones", "Phone Parts"),
    ("tablets", "Tablet Parts"),
    ("headphones", "Headphone Parts"),
    ("accessories", "Accessories"),
    ("smart_watch", "Smart Watch Parts"),
    ("smart_ring", "Smart Ring Parts"),
    ("other", "Other Parts"),
    ("batteries", "Batteries"),
]


class Product(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(blank=True, upload_to=get_upload_path)

    def __str__(self):
        return self.name
