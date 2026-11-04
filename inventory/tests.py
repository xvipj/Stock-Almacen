from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product, Variant

from .models import StockMovement


class InventoryFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(
            username="tester", password="Clave12345!"
        )
        categoria = Category.objects.create(nombre="Camisas")
        cls.producto = Product.objects.create(
            nombre="Camisa Test",
            sku="CAM-TEST-9",
            categoria=categoria,
            precio="50000.00",
        )
        cls.variante = Variant.objects.create(
            producto=cls.producto,
            talla="M",
            color="Azul",
            stock_minimo=2,
        )

    def setUp(self):
        self.client.force_login(self.usuario)
        cache.clear()

    def _registrar(self, tipo, cantidad):
        return self.client.post(
            reverse("inventory:movement_create"),
            {
                "variante": self.variante.pk,
                "tipo": tipo,
                "cantidad": cantidad,
                "nota": "Prueba",
            },
        )

    def test_entrada_y_salida_actualizan_el_stock(self):
        self.assertEqual(self._registrar("ENTRADA", 10).status_code, 302)
        self.assertEqual(self._registrar("SALIDA", 4).status_code, 302)
        self.variante.refresh_from_db()
        self.assertEqual(self.variante.stock_actual, 6)

    def test_salida_no_deja_stock_negativo(self):
        self._registrar("ENTRADA", 3)
        respuesta = self._registrar("SALIDA", 10)

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Stock insuficiente")
        self.assertEqual(self.variante.stock_actual, 3)
        self.assertEqual(StockMovement.objects.count(), 1)

    def test_ajuste_fija_el_stock_exacto(self):
        self._registrar("ENTRADA", 10)
        self._registrar("AJUSTE", 4)
        self.assertEqual(self.variante.stock_actual, 4)

    def test_movimiento_invalida_cache_del_dashboard(self):
        cache.set(settings.DASHBOARD_CACHE_KEY, {"total_unidades": 999}, 60)
        self._registrar("ENTRADA", 5)
        self.assertIsNone(cache.get(settings.DASHBOARD_CACHE_KEY))

    def test_dashboard_usa_cache_y_se_actualiza_con_un_movimiento(self):
        self._registrar("ENTRADA", 5)

        primera = self.client.get(reverse("dashboard:home"))
        segunda = self.client.get(reverse("dashboard:home"))
        self.assertFalse(primera.context["cache_usada"])
        self.assertTrue(segunda.context["cache_usada"])
        self.assertEqual(segunda.context["total_unidades"], 5)

        self._registrar("SALIDA", 2)
        tercera = self.client.get(reverse("dashboard:home"))
        self.assertFalse(tercera.context["cache_usada"])
        self.assertEqual(tercera.context["total_unidades"], 3)
