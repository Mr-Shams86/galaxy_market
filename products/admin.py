from django.contrib import admin
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "description")
    search_fields = ("description",)
    list_editable = ("price", "description")
    actions = ["make_zero"]

    @admin.action(description="Установить цену в 0")
    def make_zero(self, request, queryset):
        queryset.update(price=0)
