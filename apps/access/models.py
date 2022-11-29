from django.db import models

class Empresa(models.Model):
    nombre = models.TextField(blank=True, null=True)
    mision = models.TextField(blank=True, null=True)
    vision = models.TextField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    id_empresa = models.ForeignKey('Medico', models.DO_NOTHING, db_column='id_empresa', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'empresa'


class Medico(models.Model):
    nombres = models.CharField(max_length=50, blank=True, null=True)
    apellidos = models.CharField(max_length=50, blank=True, null=True)
    cedula_field = models.CharField(db_column='cedula ', max_length=15, blank=True, null=True)  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    correo = models.CharField(max_length=30, blank=True, null=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'medico'
