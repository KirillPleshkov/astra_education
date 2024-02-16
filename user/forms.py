from django.forms import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model

user_model = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Форма создания пользователя для админ панели с подтверждением паролей"""
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Повтор пароля')

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_email(self):
        """Проверка на попытку создания пользователя с повторяющейся почтой"""
        email = self.cleaned_data.get('email')
        qs = user_model.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Пользователь с таким email уже существует")
        return email

    def clean(self):
        """Проверка на совпадение паролей"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 is not None and password1 != password2:
            self.add_error("password2", "Пароли не совпадают")
        return cleaned_data

    def save(self, commit=True):
        """Сохранение пользователя с подменой пароля на хэшированный"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    """Форма кастомизации пользователя"""
    class Meta:
        model = CustomUser
        fields = ('email',)
