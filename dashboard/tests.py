from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product, Variant
from inventory.services import registrar_movimiento

Usuario = get_user_model()


class DashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = Usuario.objects.create_user(
            username="tester", password="Clave12345!"
        )
        categoria = Category.objects.create(nombre="Camisas")

        cls.producto_bajo = Product.objects.create(
            nombre="Camisa Baja",
            sku="CAM-BAJA",
            categoria=categoria,
            precio="50000.00",
        )
        cls.variante_baja = Variant.objects.create(
            producto=cls.producto_bajo,
            talla="M",
            color="Azul",
            stock_minimo=5,
        )

        cls.producto_sano = Product.objects.create(
            nombre="Pantalón Sano",
            sku="PAN-SANO",
            categoria=categoria,
            precio="80000.00",
        )
        cls.variante_sana = Variant.objects.create(
            producto=cls.producto_sano,
            talla="32",
            color="Negro",
            stock_minimo=1,
        )

        cls.producto_minimo = Product.objects.create(
            nombre="Chaqueta Mínima",
            sku="CHA-MIN",
            categoria=categoria,
            precio="120000.00",
        )
        cls.variante_minima = Variant.objects.create(
            producto=cls.producto_minimo,
            talla="Única",
            color="Verde",
            stock_minimo=2,
        )

        registrar_movimiento(
            variante=cls.variante_baja,
            tipo="ENTRADA",
            cantidad=1,
            usuario=cls.usuario,
            nota="Reposición parcial",
        )
        registrar_movimiento(
            variante=cls.variante_sana,
            tipo="ENTRADA",
            cantidad=10,
            usuario=cls.usuario,
            nota="Reposición",
        )
        registrar_movimiento(
            variante=cls.variante_minima,
            tipo="ENTRADA",
            cantidad=2,
            usuario=cls.usuario,
            nota="Compra",
        )

    def setUp(self):
        # LocMemCache persiste entre métodos de TestCase.
        cache.clear()
        self.client.force_login(self.usuario)

    def test_dashboard_calcula_lo_que_falta_reponer(self):
        respuesta = self.client.get(reverse("dashboard:home"))

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["total_bajos"], 2)
        self.assertEqual(respuesta.context["variantes_bajas"][0]["faltante"], 4)
        self.assertEqual(respuesta.context["variantes_bajas"][1]["faltante"], 0)
        self.assertTrue(respuesta.context["actualizado_en"])

    def test_dashboard_enlaza_al_stock_bajo_completo(self):
        respuesta = self.client.get(reverse("dashboard:home"))

        self.assertContains(respuesta, reverse("dashboard:stock_bajo"))
        self.assertContains(respuesta, "faltan 4")

    def test_stock_bajo_lista_solo_variantes_bajas_ordenadas_por_faltante(self):
        respuesta = self.client.get(reverse("dashboard:stock_bajo"))

        self.assertEqual(respuesta.status_code, 200)
        self.assertEqual(respuesta.context["total_bajos"], 2)
        self.assertEqual(respuesta.context["total_faltantes"], 4)
        nombres = [v.producto.nombre for v in respuesta.context["variantes"]]
        self.assertEqual(nombres, ["Camisa Baja", "Chaqueta Mínima"])
        self.assertNotContains(respuesta, "Pantalón Sano")
        self.assertContains(respuesta, "en mínimo")

    def test_stock_bajo_exige_sesion(self):
        self.client.logout()

        respuesta = self.client.get(reverse("dashboard:stock_bajo"))

        self.assertEqual(respuesta.status_code, 302)
        self.assertIn(reverse("accounts:login"), respuesta.url)
