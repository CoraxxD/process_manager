from django import forms
from django.contrib.auth.forms import AuthenticationForm

class BlacklistForm(forms.Form):
    process_name = forms.CharField(label='Blacklisted Process')

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
