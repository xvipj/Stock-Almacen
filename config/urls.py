from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "Stock Almacén · Administración"
admin.site.site_title = "Stock Almacén"
admin.site.index_title = "Panel de administración"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("catalogo/", include("catalog.urls")),
    path("inventario/", include("inventory.urls")),
    path("", include("dashboard.urls")),
]
