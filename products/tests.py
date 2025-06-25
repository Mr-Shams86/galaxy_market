from django.test import Client, TestCase
from django.contrib.auth.models import User
from .models import Product
from django.urls import reverse
from products.models import Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")

    def test_product_creation(self):
        product = Product.objects.create(
            seller=self.user,
            name="Test Product",
            price=100,
            description="Test description",
        )
        self.assertEqual(product.name, "Test Product")
        self.assertEqual(product.price, 100)
        self.assertEqual(str(product), "Test Product")


class CheckoutAndCBVTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.owner = User.objects.create_user(username="owner", password="123")
        self.other = User.objects.create_user(username="hacker", password="123")
        self.product = Product.objects.create(
            seller=self.owner, name="Test Product", price=50, description="Nice one"
        )

    def test_checkout_requires_login(self):
        url = reverse("products:api_checkout_session", args=[self.product.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_update_allowed_for_owner(self):
        self.client.login(username="owner", password="123")
        url = reverse("products:update_item", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_forbidden_for_others(self):
        self.client.login(username="hacker", password="123")
        url = reverse("products:update_item", args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
