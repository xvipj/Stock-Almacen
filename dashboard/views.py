from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db.models import Prefetch
from django.shortcuts import render

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
    cache_usada = resumen is not None

    if resumen is None:
        resumen = _calcular_resumen()
        cache.set(
            settings.DASHBOARD_CACHE_KEY,
            resumen,
            settings.DASHBOARD_CACHE_TIMEOUT,
        )

    return render(
        request,
        "dashboard/home.html",
        {**resumen, "cache_usada": cache_usada},
    )
