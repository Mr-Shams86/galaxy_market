from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models.user import CustomUser
from .models import Profile


# -------------------------
# Регистрация пользователя
# -------------------------


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(
            attrs={"class": "focus:outline-none", "placeholder": "mail@mail.com"}
        ),
        label="Email",
        help_text="Введите рабочий email — он будет использоваться как логин",
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "focus:outline-none", "placeholder": "Введите пароль"}
        ),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "focus:outline-none", "placeholder": "Повторите пароль"}
        ),
    )

    class Meta:
        model = CustomUser
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже используется.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# -------------------------
# Форма профиля
# -------------------------


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["nickname", "bio", "avatar", "contact_number"]
        labels = {
            "nickname": "Никнейм",
            "bio": "О себе",
            "avatar": "Фото профиля",
            "contact_number": "Контактный номер",
        }
        widgets = {
            "nickname": forms.TextInput(
                attrs={"class": "focus:outline-none", "placeholder": "Введите никнейм"}
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "focus:outline-none",
                    "placeholder": "Опишите себя (до 500 символов)",
                }
            ),
            "avatar": forms.ClearableFileInput(attrs={"class": "focus:outline-none"}),
            "contact_number": forms.TextInput(
                attrs={"class": "focus:outline-none", "placeholder": "+998901234567"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].required = False
        self.fields["nickname"].required = True

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile

    def clean_contact_number(self):
        contact_number = self.cleaned_data["contact_number"]
        if not contact_number.startswith("+998"):
            raise forms.ValidationError("Номер должен начинаться с +998")
        return contact_number

    def clean_bio(self):
        bio = self.cleaned_data["bio"]
        if len(bio) > 500:
            raise forms.ValidationError("Описание не должно превышать 500 символов")
        return bio

    def clean_nickname(self):
        nickname = self.cleaned_data["nickname"]
        if (
            Profile.objects.filter(nickname=nickname)
            .exclude(pk=self.instance.pk)
            .exists()
        ):
            raise forms.ValidationError("Этот никнейм уже занят.")
        return nickname
