from django.db import models
from .product import Product


class OrderDetail(models.Model):
    customer_username = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_payment_intent = models.CharField(max_length=200, null=True, blank=True)
    has_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.customer_username} — {self.product.name} — {self.amount}"
