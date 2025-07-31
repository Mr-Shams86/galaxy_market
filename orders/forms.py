# orders/forms.py
from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=100)
    phone = forms.CharField(label="Телефон", max_length=20)
    address = forms.CharField(label="Адрес", widget=forms.Textarea)
