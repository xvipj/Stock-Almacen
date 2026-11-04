from django.contrib import admin

from .models import StockMovement


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ("fecha", "variante", "tipo", "cantidad", "usuario")
    list_filter = ("tipo", "fecha", "variante__producto__categoria", "usuario")
    search_fields = (
        "variante__producto__nombre",
        "variante__producto__sku",
        "variante__talla",
        "variante__color",
        "nota",
        "usuario__username",
    )
    list_select_related = ("variante__producto", "usuario")
    autocomplete_fields = ("variante", "usuario")
    date_hierarchy = "fecha"
    readonly_fields = ("fecha",)
