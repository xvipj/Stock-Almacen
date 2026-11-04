from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .forms import LoginForm

app_name = "accounts"

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=LoginForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    # LogoutView solo acepta POST desde Django 5 (el formulario del menú lo envía).
    path("logout/", LogoutView.as_view(), name="logout"),
]
