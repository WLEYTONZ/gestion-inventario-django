from django.test import TestCase
from django.urls import reverse

from .models import Categoria, Producto


class ProductoCrudTests(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Tecnología")
        self.producto = Producto.objects.create(
            codigo="TEC-001", nombre="Teclado", descripcion="Teclado para computador", categoria=self.categoria,
            precio="89.90", stock=10,
        )

    def test_lista_muestra_producto(self):
        response = self.client.get(reverse("inventario:producto_lista"))
        self.assertContains(response, self.producto.nombre)

    def test_crear_producto_valido(self):
        response = self.client.post(reverse("inventario:producto_crear"), {
            "codigo": "TEC-002", "nombre": "Mouse", "descripcion": "Mouse óptico", "categoria": self.categoria.pk,
            "precio": "45.50", "stock": 5,
        })
        self.assertRedirects(response, reverse("inventario:producto_lista"))
        self.assertTrue(Producto.objects.filter(codigo="TEC-002").exists())

    def test_crear_rechaza_precio_no_positivo(self):
        response = self.client.post(reverse("inventario:producto_crear"), {
            "codigo": "TEC-003", "nombre": "Monitor", "descripcion": "Monitor LED", "categoria": self.categoria.pk,
            "precio": "0", "stock": 5,
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Producto.objects.filter(codigo="TEC-003").exists())

    def test_editar_producto(self):
        response = self.client.post(reverse("inventario:producto_editar", args=[self.producto.pk]), {
            "codigo": "TEC-001", "nombre": "Teclado mecánico", "descripcion": "Teclado mecánico", "categoria": self.categoria.pk,
            "precio": "100.00", "stock": 12,
        })
        self.assertRedirects(response, reverse("inventario:producto_lista"))
        self.producto.refresh_from_db()
        self.assertEqual(self.producto.nombre, "Teclado mecánico")

    def test_buscar_por_codigo_o_nombre(self):
        response = self.client.get(reverse("inventario:producto_lista"), {"q": "TEC-001"})
        self.assertContains(response, self.producto.nombre)

    def test_eliminar_producto_solo_post(self):
        url = reverse("inventario:producto_eliminar", args=[self.producto.pk])
        self.assertEqual(self.client.get(url).status_code, 200)
        self.assertTrue(Producto.objects.filter(pk=self.producto.pk).exists())
        response = self.client.post(url)
        self.assertRedirects(response, reverse("inventario:producto_lista"))
        self.assertFalse(Producto.objects.filter(pk=self.producto.pk).exists())
