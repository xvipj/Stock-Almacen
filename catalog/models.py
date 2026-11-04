from django.db import models
from django.urls import reverse

from inventory.stock import calcular_stock


class Category(models.Model):
    """Agrupación simple de productos (camisas, pantalones, etc.)."""

    nombre = models.CharField("nombre", max_length=80, unique=True)

    class Meta:
        verbose_name = "categoría"
        verbose_name_plural = "categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Product(models.Model):
    """Producto del catálogo. El stock vive en sus variantes."""

    nombre = models.CharField("nombre", max_length=120)
    sku = models.CharField("SKU", max_length=40, unique=True)
    categoria = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="productos",
        verbose_name="categoría",
    )
    marca = models.CharField("marca", max_length=80, blank=True)
    precio = models.DecimalField("precio", max_digits=10, decimal_places=2)
    activo = models.BooleanField("activo", default=True)
    creado_en = models.DateTimeField("fecha de creación", auto_now_add=True)

    class Meta:
        verbose_name = "producto"
        verbose_name_plural = "productos"
        ordering = ["nombre"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(precio__gte=0),
                name="producto_precio_no_negativo",
            )
        ]

    def __str__(self):
        return f"{self.nombre} ({self.sku})"

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.pk])

    @property
    def stock_total(self):
        """Suma el stock de todas las variantes (usa el prefetch si existe)."""
        return sum(variante.stock_actual for variante in self.variantes.all())

    @property
    def tiene_stock_bajo(self):
        return any(variante.stock_bajo for variante in self.variantes.all())


class Variant(models.Model):
    """Combinación talla + color de un producto. Aquí se controla el stock."""

    producto = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variantes",
        verbose_name="producto",
    )
    talla = models.CharField("talla", max_length=10)
    color = models.CharField("color", max_length=30)
    stock_minimo = models.PositiveIntegerField("stock mínimo", default=0)

    class Meta:
        verbose_name = "variante"
        verbose_name_plural = "variantes"
        ordering = ["producto__nombre", "talla", "color"]
        constraints = [
            models.UniqueConstraint(
                fields=["producto", "talla", "color"],
                name="variante_unica_por_producto_talla_color",
            )
        ]

    def __str__(self):
        return f"{self.producto.nombre} · {self.talla} / {self.color}"

    def get_absolute_url(self):
        return reverse("catalog:product_detail", args=[self.producto_id])

    @property
    def stock_actual(self):
        """El stock nunca se guarda: se calcula desde los movimientos."""
        return calcular_stock(self.movimientos.all())

    @property
    def stock_bajo(self):
        return self.stock_actual <= self.stock_minimo
