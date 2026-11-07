from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.shortcuts import render
from django.utils import timezone

from catalog.models import Product, Variant
from inventory.models import StockMovement


def _calcular_resumen():
    """Consulta la base de datos y devuelve datos simples (serializables)."""
    variantes = list(
        Variant.objects.filter(producto__activo=True)
        .select_related("producto")
        .prefetch_related(
            Prefetch(
                "movimientos",
                queryset=StockMovement.objects.order_by("fecha", "pk"),
            )
        )
    )

    variantes_bajas = [v for v in variantes if v.stock_bajo]
    variantes_bajas.sort(key=lambda v: (v.stock_actual - v.stock_minimo, v.producto.nombre))

    movimientos = (
        StockMovement.objects.select_related("variante__producto", "usuario")
        .order_by("-fecha", "-pk")[:10]
    )

    return {
        "generado_en": timezone.now(),
        "total_productos": Product.objects.filter(activo=True).count(),
        "total_variantes": len(variantes),
        "total_unidades": sum(v.stock_actual for v in variantes),
        "total_bajos": len(variantes_bajas),
        "variantes_bajas": [
            {
                "producto_id": v.producto_id,
                "producto": v.producto.nombre,
                "talla": v.talla,
                "color": v.color,
                "stock": v.stock_actual,
                "minimo": v.stock_minimo,
                "faltante": max(v.stock_minimo - v.stock_actual, 0),
            }
            for v in variantes_bajas[:5]
        ],
        "movimientos": [
            {
                "id": m.pk,
                "producto_id": m.variante.producto_id,
                "producto": m.variante.producto.nombre,
                "variante": f"{m.variante.talla} / {m.variante.color}",
                "tipo": m.tipo,
                "tipo_display": m.get_tipo_display(),
                "cantidad": m.cantidad,
                "cantidad_con_signo": m.cantidad_con_signo,
                "usuario": m.usuario.get_username(),
                "fecha": m.fecha,
            }
            for m in movimientos
        ],
    }


@login_required
def home(request):
    resumen = cache.get(settings.DASHBOARD_CACHE_KEY)
    cache_usada = bool(resumen) and "generado_en" in resumen

    # La forma del resumen cambió (se agregó generado_en y faltante); si hay
    # una entrada vieja en caché, se recalcula en lugar de mostrar datos incompletos.
    if not cache_usada:
        resumen = _calcular_resumen()
        cache.set(
            settings.DASHBOARD_CACHE_KEY,
            resumen,
            settings.DASHBOARD_CACHE_TIMEOUT,
        )

    return render(
        request,
        "dashboard/home.html",
        {
            **resumen,
            "actualizado_en": resumen["generado_en"],
            "cache_usada": cache_usada,
        },
    )


@login_required
def stock_bajo(request):
    """Lista completa de variantes en o por debajo de su stock mínimo."""
    variantes = list(
        Variant.objects.filter(producto__activo=True)
        .select_related("producto")
        .prefetch_related(
            Prefetch(
                "movimientos",
                queryset=StockMovement.objects.order_by("fecha", "pk"),
            )
        )
    )

    bajas = [v for v in variantes if v.stock_bajo]
    for variante in bajas:
        variante.faltante = max(variante.stock_minimo - variante.stock_actual, 0)
    # Primero lo que más falta reponer.
    bajas.sort(key=lambda v: (-v.faltante, v.producto.nombre, v.talla, v.color))

    paginator = Paginator(bajas, 30)
    pagina = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "dashboard/stock_bajo.html",
        {
            "variantes": pagina,
            "paginator": paginator,
            "page_obj": pagina,
            "is_paginated": pagina.has_other_pages(),
            "total_bajos": len(bajas),
            "total_faltantes": sum(v.faltante for v in bajas),
        },
    )
