from django.apps import AppConfig


class InventoryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "inventory"
    verbose_name = "Inventario"

    def ready(self):
        # Registra la señal que invalida la caché al crear/borrar movimientos.
        from . import signals  # noqa: F401
