from django.db import models
from django.core.validators import MinValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre de Categoría")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

class Producto(models.Model):
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código del Producto")
    nombre = models.CharField(max_length=150, verbose_name="Nombre del Producto")
    descripcion = models.TextField(verbose_name="Descripción")
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos", verbose_name="Categoría")
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)], verbose_name="Precio ($)")
    stock = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Cantidad en Stock")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['-fecha_creacion']
