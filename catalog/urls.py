from django.urls import path

from . import views

app_name = "catalog"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("nuevo/", views.ProductCreateView.as_view(), name="product_create"),
    # Las rutas de variantes van antes de <int:pk>/ para que sean más explícitas.
    path(
        "<int:product_pk>/variantes/nueva/",
        views.VariantCreateView.as_view(),
        name="variant_create",
    ),
    path(
        "variantes/<int:pk>/editar/",
        views.VariantUpdateView.as_view(),
        name="variant_update",
    ),
    path(
        "variantes/<int:pk>/eliminar/",
        views.VariantDeleteView.as_view(),
        name="variant_delete",
    ),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("<int:pk>/editar/", views.ProductUpdateView.as_view(), name="product_update"),
    path("<int:pk>/eliminar/", views.ProductDeleteView.as_view(), name="product_delete"),
]
