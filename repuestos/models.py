from django.db import models

# Create your models here.
class Repuesto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre del Repuesto')
    categoria = models.CharField(max_length=50, verbose_name='Categoría')
    precio = models.IntegerField(verbose_name='Precio')
    stock = models.IntegerField(verbose_name='Cantidad en Stock')
    imagen = models.ImageField(upload_to='imagenes/', verbose_name='Imagen', null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"

    def delete(self, using=None, keep_parents=False):
        if self.imagen:
            self.imagen.storage.delete(self.imagen.name)
        super().delete()
