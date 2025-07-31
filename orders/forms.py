from django import forms

class CheckoutForm(forms.Form):
    name = forms.CharField(
        label="Имя",
        max_length=100,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 rounded-lg border border-gray-300 bg-white text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500",
            "placeholder": "Введите ваше имя"
        })
    )
    phone = forms.CharField(
        label="Телефон",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-2 rounded-lg border border-gray-300 bg-white text-black placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-green-500",
            "placeholder": "Ваш номер телефона"
        })
    )
    address = forms.CharField(
        label="Адрес",
        widget=forms.Textarea(attrs={
            "class": "w-full px-4 py-2 rounded-lg border border-gray-300 bg-white text-black placeholder-gray-500 resize-none focus:outline-none focus:ring-2 focus:ring-green-500",
            "rows": 3,
            "placeholder": "Укажите адрес доставки"
        })
    )
