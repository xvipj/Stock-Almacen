from django import forms
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    """AuthenticationForm con textos y atributos pensados para la interfaz."""

    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Tu nombre de usuario",
                "autofocus": True,
                "autocomplete": "username",
            }
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "••••••••",
                "autocomplete": "current-password",
            }
        ),
    )
