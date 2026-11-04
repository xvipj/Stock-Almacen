from django.conf import settings
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Product, Variant


@receiver([post_save, post_delete], sender=Product)
@receiver([post_save, post_delete], sender=Variant)
def invalidar_resumen_dashboard(sender, **kwargs):
    """Crear, editar o borrar productos/variantes también cambia los totales."""
    cache.delete(settings.DASHBOARD_CACHE_KEY)
