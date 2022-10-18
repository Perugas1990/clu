from django.db import models
from apps.cliente.models import Usuario
# Create your models here.
class Agenda(models.Model):
    
    cliente = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    fecha_desde = models.DateTimeField(blank=False, null=False)
    fecha_hasta = models.DateTimeField(blank=False, null=False)
    comentario = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=100,blank=True, null=True)
    created = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    

    class Meta:
        managed = False
        db_table = 'agenda'

    def __str__(self):
        return self.comentario