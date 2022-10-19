from django.db import models



# Create your models here.
class Insumos(models.Model):
    
    nombre = models.CharField('Nombre', max_length=100, blank=False, null=False)
    detalle = models.CharField('Detalle', max_length=200, blank=False, null=False)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre 

    class Meta:
        managed = False
        db_table = 'insumos'