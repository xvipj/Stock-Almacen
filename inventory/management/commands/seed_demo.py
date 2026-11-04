from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from catalog.models import Category, Product, Variant
from inventory.models import StockMovement

# Cada movimiento es (tipo, cantidad, nota).
# El AJUSTE fija el stock exacto al valor indicado.
CATEGORIAS = ["Camisas", "Pantalones", "Chaquetas", "Accesorios"]

PRODUCTOS = [
    {
        "nombre": "Camisa Oxford",
        "sku": "CAM-OXF-001",
        "categoria": "Camisas",
        "marca": "Andina",
        "precio": Decimal("89900.00"),
        "variantes": [
            {"talla": "S", "color": "Azul", "minimo": 3, "movimientos": [("ENTRADA", 12, "Carga inicial de proveedor"), ("SALIDA", 3, "Venta mostrador")]},
            {"talla": "M", "color": "Azul", "minimo": 3, "movimientos": [("ENTRADA", 15, "Carga inicial de proveedor"), ("SALIDA", 11, "Pedido online")]},
            {"talla": "L", "color": "Blanco", "minimo": 2, "movimientos": [("ENTRADA", 4, "Reposición"), ("SALIDA", 3, "Venta mostrador")]},
        ],
    },
    {
        "nombre": "Camiseta Básica",
        "sku": "CAM-BAS-002",
        "categoria": "Camisas",
        "marca": "Básicos",
        "precio": Decimal("49900.00"),
        "variantes": [
            {"talla": "S", "color": "Negro", "minimo": 5, "movimientos": [("ENTRADA", 20, "Carga inicial"), ("SALIDA", 8, "Venta mostrador")]},
            {"talla": "M", "color": "Blanco", "minimo": 5, "movimientos": [("ENTRADA", 18, "Carga inicial"), ("SALIDA", 10, "Venta mostrador")]},
            {"talla": "L", "color": "Gris", "minimo": 4, "movimientos": [("ENTRADA", 10, "Carga inicial"), ("SALIDA", 9, "Liquidación")]},
        ],
    },
    {
        "nombre": "Jean Recto",
        "sku": "JEA-REC-003",
        "categoria": "Pantalones",
        "marca": "Denim Co",
        "precio": Decimal("129900.00"),
        "variantes": [
            {"talla": "30", "color": "Azul oscuro", "minimo": 2, "movimientos": [("ENTRADA", 10, "Carga inicial"), ("SALIDA", 4, "Venta mostrador")]},
            {"talla": "32", "color": "Azul oscuro", "minimo": 2, "movimientos": [("ENTRADA", 8, "Carga inicial"), ("SALIDA", 6, "Pedido online")]},
            {"talla": "34", "color": "Negro", "minimo": 2, "movimientos": [("ENTRADA", 6, "Carga inicial"), ("SALIDA", 5, "Venta mostrador"), ("AJUSTE", 4, "Conteo físico: quedan 4")]},
        ],
    },
    {
        "nombre": "Chaqueta Cortavientos",
        "sku": "CHA-COR-004",
        "categoria": "Chaquetas",
        "marca": "Andina",
        "precio": Decimal("189900.00"),
        "variantes": [
            {"talla": "M", "color": "Verde oliva", "minimo": 3, "movimientos": [("ENTRADA", 8, "Carga inicial"), ("SALIDA", 2, "Venta mostrador")]},
            {"talla": "L", "color": "Negro", "minimo": 3, "movimientos": [("ENTRADA", 5, "Carga inicial"), ("SALIDA", 3, "Pedido online")]},
        ],
    },
    {
        "nombre": "Bufanda de Lana",
        "sku": "BUF-LAN-005",
        "categoria": "Accesorios",
        "marca": "Norte",
        "precio": Decimal("39900.00"),
        "variantes": [
            {"talla": "Única", "color": "Beige", "minimo": 4, "movimientos": [("ENTRADA", 25, "Carga inicial"), ("SALIDA", 5, "Venta de temporada")]},
        ],
    },
    {
        "nombre": "Gorra Clásica",
        "sku": "GOR-CLA-006",
        "categoria": "Accesorios",
        "marca": "Norte",
        "precio": Decimal("29900.00"),
        "variantes": [
            {"talla": "Única", "color": "Negro", "minimo": 5, "movimientos": [("ENTRADA", 12, "Carga inicial"), ("SALIDA", 7, "Venta mostrador")]},
            {"talla": "Única", "color": "Azul", "minimo": 5, "movimientos": [("ENTRADA", 6, "Carga inicial"), ("SALIDA", 2, "Venta mostrador")]},
        ],
    },
    {
        "nombre": "Polo Vintage",
        "sku": "POL-VIN-007",
        "categoria": "Camisas",
        "marca": "Retro",
        "precio": Decimal("59900.00"),
        "activo": False,
        "variantes": [],
    },
]


class Command(BaseCommand):
    help = "Crea datos de ejemplo para probar el sistema de stock."

    def handle(self, *args, **options):
        usuario = self._obtener_usuario()
        ahora = timezone.now()
        dias = 45

        categorias = {}
        for nombre in CATEGORIAS:
            categoria, _ = Category.objects.get_or_create(nombre=nombre)
            categorias[nombre] = categoria

        productos_creados = 0
        variantes_creadas = 0
        movimientos_creados = 0

        for datos in PRODUCTOS:
            producto, creado = Product.objects.get_or_create(
                sku=datos["sku"],
                defaults={
                    "nombre": datos["nombre"],
                    "categoria": categorias[datos["categoria"]],
                    "marca": datos.get("marca", ""),
                    "precio": datos["precio"],
                    "activo": datos.get("activo", True),
                },
            )
            if creado:
                productos_creados += 1

            for datos_variante in datos["variantes"]:
                variante, creada = Variant.objects.get_or_create(
                    producto=producto,
                    talla=datos_variante["talla"],
                    color=datos_variante["color"],
                    defaults={"stock_minimo": datos_variante["minimo"]},
                )
                if creada:
                    variantes_creadas += 1

                # Si la variante ya tiene movimientos, no duplicamos el demo.
                if StockMovement.objects.filter(variante=variante).exists():
                    continue

                for tipo, cantidad, nota in datos_variante["movimientos"]:
                    movimiento = StockMovement(
                        variante=variante,
                        tipo=tipo,
                        cantidad=cantidad,
                        nota=nota,
                        usuario=usuario,
                    )
                    movimiento.save()

                    # auto_now_add ignora fechas manuales al crear; las ajustamos
                    # después para que el historial se vea distribuido en el tiempo.
                    StockMovement.objects.filter(pk=movimiento.pk).update(
                        fecha=ahora - timedelta(days=dias, hours=movimientos_creados % 7)
                    )
                    movimientos_creados += 1
                    dias -= 1

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Datos de demostración listos:"))
        self.stdout.write(f"  · Categorías: {len(categorias)}")
        self.stdout.write(f"  · Productos nuevos: {productos_creados}")
        self.stdout.write(f"  · Variantes nuevas: {variantes_creadas}")
        self.stdout.write(f"  · Movimientos nuevos: {movimientos_creados}")
        self.stdout.write("")
        self.stdout.write("Ejecuta el servidor con: python manage.py runserver")

    def _obtener_usuario(self):
        """Usa el primer superusuario; si no existe, crea un usuario de sistema."""
        Usuario = get_user_model()
        usuario = Usuario.objects.filter(is_superuser=True).order_by("pk").first()
        if usuario:
            return usuario

        usuario, creado = Usuario.objects.get_or_create(
            username="bodega",
            defaults={"email": "bodega@example.com", "first_name": "Bodega"},
        )
        if creado:
            usuario.set_unusable_password()
            usuario.save()
        return usuario
