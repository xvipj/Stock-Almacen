from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Variant


class CatalogViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.usuario = get_user_model().objects.create_user(
            username="tester", password="Clave12345!"
        )
        cls.categoria = Category.objects.create(nombre="Camisas")

    def setUp(self):
        self.client.force_login(self.usuario)

    def test_catalogo_requiere_login(self):
        self.client.logout()
        respuesta = self.client.get(reverse("catalog:product_list"))
        self.assertEqual(respuesta.status_code, 302)
        self.assertIn(reverse("accounts:login"), respuesta.url)

    def test_crear_producto_normaliza_sku(self):
        respuesta = self.client.post(
            reverse("catalog:product_create"),
            {
                "nombre": "Camisa Test",
                "sku": " cam-test-1 ",
                "categoria": self.categoria.pk,
                "marca": "Marca",
                "precio": "89900.00",
                "activo": "on",
            },
        )
        self.assertEqual(respuesta.status_code, 302)
        producto = Product.objects.get(sku="CAM-TEST-1")
        self.assertEqual(producto.nombre, "Camisa Test")

    def test_variante_unica_por_producto_talla_color(self):
        producto = Product.objects.create(
            nombre="Camisa Test",
            sku="CAM-TEST-2",
            categoria=self.categoria,
            precio="50000.00",
        )
        url = reverse("catalog:variant_create", args=[producto.pk])
        datos = {"talla": "m", "color": "azul", "stock_minimo": 3}

        primera = self.client.post(url, datos)
        segunda = self.client.post(url, datos)

        self.assertEqual(primera.status_code, 302)
        self.assertEqual(segunda.status_code, 200)
        self.assertEqual(producto.variantes.count(), 1)
        variante = Variant.objects.get(producto=producto)
        self.assertEqual(variante.talla, "M")
        self.assertEqual(variante.color, "Azul")
