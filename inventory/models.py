from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

from catalog.models import Variant

from .stock import AJUSTE, ENTRADA, SALIDA, calcular_stock


class StockMovement(models.Model):
    """Movimiento de inventario. Es la única fuente de verdad del stock."""

    class Tipo(models.TextChoices):
        ENTRADA = ENTRADA, "Entrada"
        SALIDA = SALIDA, "Salida"
        AJUSTE = AJUSTE, "Ajuste"

    variante = models.ForeignKey(
        Variant,
        on_delete=models.CASCADE,
        related_name="movimientos",
        verbose_name="variante",
    )
    tipo = models.CharField("tipo", max_length=10, choices=Tipo.choices)
    cantidad = models.PositiveIntegerField(
        "cantidad",
        help_text="En un ajuste, es el stock final deseado (ej. 12).",
    )
    nota = models.TextField("nota", blank=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="movimientos_stock",
        verbose_name="usuario",
    )
    fecha = models.DateTimeField("fecha", auto_now_add=True)

    class Meta:
        verbose_name = "movimiento de stock"
        verbose_name_plural = "movimientos de stock"
        ordering = ["-fecha", "-pk"]

    def __str__(self):
        return f"{self.get_tipo_display()} · {self.variante} · {self.cantidad}"

    @property
    def cantidad_con_signo(self):
        """Texto corto para mostrar el efecto del movimiento en las tablas."""
        if self.tipo == self.Tipo.ENTRADA:
            return f"+{self.cantidad}"
        if self.tipo == self.Tipo.SALIDA:
            return f"-{self.cantidad}"
        return f"={self.cantidad}"

    def clean(self):
        # Las entradas y salidas deben mover al menos una unidad.
        if self.tipo in (self.Tipo.ENTRADA, self.Tipo.SALIDA) and not self.cantidad:
            raise ValidationError({"cantidad": "La cantidad debe ser mayor que cero."})

        # Una salida nunca puede dejar el stock negativo.
        if self.tipo == self.Tipo.SALIDA and self.variante_id and self.cantidad:
            movimientos = self.variante.movimientos.all()
            if self.pk:
                # Al editar, el propio movimiento no debe contar dos veces.
                movimientos = movimientos.exclude(pk=self.pk)
            disponible = calcular_stock(movimientos)
            if self.cantidad > disponible:
                raise ValidationError(
                    {
                        "cantidad": (
                            f"Stock insuficiente: solo hay {disponible} unidades "
                            "disponibles para esta variante."
                        )
                    }
                )

    def save(self, *args, **kwargs):
        # Validamos también cuando se crea desde el admin, el shell o un comando.
        self.full_clean()
        return super().save(*args, **kwargs)
