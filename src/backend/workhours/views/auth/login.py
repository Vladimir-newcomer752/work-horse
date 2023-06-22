from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.utils.translation import pgettext_lazy

from utility.mixins import GenericMixin


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Адрес электронной почты',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш адрес электронной почты',
            'autofocus': True
        }))
    password = forms.CharField(
        label='Пароль',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control form-control-appended',
            'placeholder': 'Введите свой пароль'
        }))


class LoginView(GenericMixin,
                DjangoLoginView):
    authentication_form = LoginForm
    page_title_1 = 'Авторизоваться'
    page_title_2 = 'Введите свои регистрационные данные'
    template_name = 'workhours/auth/login.html'

    def get_success_url(self):
        if next_page := (self.request.GET.get('next') or
                         self.request.POST.get('next')):
            result = next_page
        else:
            result = reverse_lazy('workhours.home')
        return result
