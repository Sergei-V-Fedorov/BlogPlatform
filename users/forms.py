from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile
from django.utils.translation import gettext_lazy as _


class AuthForm(AuthenticationForm):
    username = forms.CharField(max_length=24, label=_('Логин'))
    password = forms.CharField(widget=forms.PasswordInput, label=_('Пароль'))


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=24, required=False, label=_('Имя'))
    last_name = forms.CharField(max_length=24, required=False, label=_('Фамилия'))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=24, required=False, label=_('Имя'))
    last_name = forms.CharField(max_length=24, required=False, label=_('Фамилия'))

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'avatar']
