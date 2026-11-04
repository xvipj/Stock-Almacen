from django.contrib import admin

from .models import Category, Product, Variant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("nombre",)
    search_fields = ("nombre",)


class VariantInline(admin.TabularInline):
    model = Variant
    extra = 1
    fields = ("talla", "color", "stock_minimo")
    show_change_link = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sku", "categoria", "marca", "precio", "activo", "stock_total")
    list_filter = ("activo", "categoria", "marca")
    search_fields = ("nombre", "sku", "marca")
    list_select_related = ("categoria",)
    inlines = [VariantInline]
    date_hierarchy = "creado_en"

    def get_queryset(self, request):
        # Precargamos variantes y movimientos para calcular el stock sin N+1.
        return (
            super()
            .get_queryset(request)
            .prefetch_related("variantes__movimientos")
        )

    @admin.display(description="Stock total")
    def stock_total(self, obj):
        return obj.stock_total


@admin.register(Variant)
class VariantAdmin(admin.ModelAdmin):
    list_display = ("producto", "talla", "color", "stock_minimo", "stock_actual", "stock_bajo")
    list_filter = ("producto__categoria", "producto", "talla", "color")
    search_fields = ("producto__nombre", "producto__sku", "talla", "color")
    list_select_related = ("producto",)
    autocomplete_fields = ("producto",)

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("producto")
            .prefetch_related("movimientos")
        )

    @admin.display(description="Stock actual")
    def stock_actual(self, obj):
        return obj.stock_actual

    @admin.display(description="¿Stock bajo?", boolean=True)
    def stock_bajo(self, obj):
        return obj.stock_bajo
