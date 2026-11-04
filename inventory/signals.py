from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import StockMovement


@receiver([post_save, post_delete], sender=StockMovement)
def invalidar_resumen_dashboard(sender, **kwargs):
    """Cada movimiento cambia los indicadores: tiramos la caché del dashboard."""
    cache.delete(settings.DASHBOARD_CACHE_KEY)
