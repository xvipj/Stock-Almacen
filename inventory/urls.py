from django.urls import path

from . import views

app_name = "inventory"

urlpatterns = [
    path("", views.MovementListView.as_view(), name="movement_list"),
    path("registrar/", views.MovementCreateView.as_view(), name="movement_create"),
]
