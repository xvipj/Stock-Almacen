from django.db import transaction

from catalog.models import Variant

from .models import StockMovement


@transaction.atomic
def registrar_movimiento(*, variante, tipo, cantidad, usuario, nota=""):
    """Punto único para crear movimientos desde las vistas de la app.

    La transacción y el bloqueo de la variante evitan que dos salidas simultáneas
    lean el mismo stock. SQLite serializa las escrituras de todos modos.
    """
    variante = Variant.objects.select_for_update().get(pk=variante.pk)
    movimiento = StockMovement(
        variante=variante,
        tipo=tipo,
        cantidad=cantidad,
        usuario=usuario,
        nota=nota,
    )
    movimiento.save()
    return movimiento
