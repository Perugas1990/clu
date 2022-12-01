from django.db import models



# Create your models here.
class Insumos(models.Model):
    id_producto = models.ForeignKey('Producto', models.DO_NOTHING, db_column='id_producto', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'insumos'



class Proveedor(models.Model):
    identificacion = models.CharField(max_length=20, blank=True, null=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=13, blank=True, null=True)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    correo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre+" "+self.apellido
    class Meta:
        managed = False
        db_table = 'proveedor'

class Producto(models.Model):
    nombre = models.CharField(max_length=150, blank=True, null=True)
    precio = models.FloatField(blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    id_proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='id_proveedor')

    
    class Meta:
        managed = False
        db_table = 'producto'
