from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Usuario(models.Model):
    opciones_genero = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('N/A', 'Ninguno'),
    )
    tipos_sangre = (
        ('1','A+'),
        ('2','A-'),
        ('3','B+'),
        ('4','B-'),
        ('5','AB+'),
        ('6','AB-'),
        ('7','O+'),
        ('8','O-'),
    )
    identificacion = models.CharField('Cedula', max_length=15, blank=False, null=False)
    nombres = models.CharField('Nombre', max_length=100, blank=False, null=False)
    apellidos = models.CharField('Apellido', max_length=100, blank=False, null=False)
    lugar_nacimiento = models.CharField('LugarN', max_length=50, blank=False, null=False)
    fecha_nacimiento = models.DateField('FechaN', blank=False, null=False)
    edad = models.IntegerField(blank=False, null=False)
    direccion = models.CharField('Direccion', max_length=300,  blank=False, null=False)
    canton = models.CharField('Canton', max_length=50, blank=False, null=False)
    provincia = models.CharField('Provincia', max_length=50, blank=False, null=False)
    pais = models.CharField('Pais', max_length=50, blank=False, null=False)
    sexo = models.CharField('Sexo',max_length=20, choices = opciones_genero)
    tipo_sangre = models.CharField('TipoS',max_length=5, choices = tipos_sangre)
    celular = models.CharField('Celular', max_length=15, blank=False, null=False)
    correo = models.EmailField()
    #Contacto emergencia
    nombre_contacto_emergencia = models.CharField('NombreE', max_length=200, blank=True, null=True)
    parentesco_contacto_emergencia = models.CharField('ParentescoE', max_length=80, blank=True, null=True)
    telefono_contacto_emergencia = models.CharField('CelularE', max_length=15, blank=True, null=True)
    #Menor de Edad
    is_menor =  models.BooleanField('Es_menor', default=False)
    nombre_tutor = models.CharField('NombreT', max_length=200, blank=True, null=True)
    parentesco_tutor = models.CharField('ParentescoT', max_length=80, blank=True, null=True)
    telefono_tutor = models.CharField('CelularT', max_length=15, blank=True, null=True)
    direccion_tutor = models.CharField('DireccionT', max_length=300, blank=True, null=True)
    username = models.CharField('Username', max_length=100, blank=False, null=False)
    def __str__(self):
        return self.nombres + ' ' + self.apellidos

    class Meta:
        managed = False
        db_table = 'usuario'


class Historial(models.Model):
    cliente = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_cliente')

    class Meta:
        managed = False
        db_table = 'historial'

class Atencion(models.Model):
    m_consulta = models.TextField(blank=True, null=True)
    enf_actual = models.TextField(blank=True, null=True)
    antecedentes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    id_historial = models.ForeignKey('Historial', models.DO_NOTHING, db_column='id_historial', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'atencion'

class Odontograma(models.Model):

    selector = (
        ('1','11'),
        ('2','12'),
        ('3','13'),
        ('4','14'),
        ('5','15'),
        ('6','16'),
        ('7','17'),
        ('8','18'),
        ('9','21'),
        ('10','22'),
        ('11','23'),
        ('12','24'),
        ('13','25'),
        ('14','26'),
        ('15','27'),
        ('16','28'),
        ('17','31'),
        ('18','32'),
        ('19','33'),
        ('20','34'),
        ('21','35'),
        ('22','36'),
        ('23','37'),
        ('24','38'),
        ('25','41'),
        ('26','42'),
        ('27','43'),
        ('28','44'),
        ('29','45'),
        ('30','46'),
        ('31','47'),
        ('32','48'),
        ('33','51'),
        ('34','52'),
        ('35','53'),
        ('36','54'),
        ('37','55'),
        ('38','61'),
        ('39','62'),
        ('40','63'),
        ('41','64'),
        ('42','65'),
        ('43','71'),
        ('44','72'),
        ('45','73'),
        ('46','74'),
        ('47','75'),
        ('48','81'),
        ('49','82'),
        ('50','83'),
        ('51','84'),
        ('52','85'),
    )
    simbologia = (
        ('1','Sellante necesario'),
        ('2','A-Sellante necesario'),
        ('3','Extraccion indicada'),
        ('4','Perdida por caries'),
        ('5','Perdida(otra causa)'),
        ('6','Endodoncia'),
        ('7','Protesis Fija'),
        ('8','Protesis removible'),
        ('9','Protesis total'),
        ('10','Corona'),
        ('11','Caries'),
        ('12','Obturado'),
    )
    id_atencion = models.ForeignKey(Atencion, models.DO_NOTHING, db_column='id_atencion', blank=True, null=True)
    diente = models.CharField('Tipos',max_length=5, choices = selector)
    detalle = models.CharField('Simmbologia',max_length=5, choices = simbologia)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'odontograma'




class Estomatogmatico(models.Model):

    selector = (
        ('1','Labios'),
        ('2','Glandulas salivales'),
        ('3','Mejilla'),
        ('4','Maxilar'),
        ('5','Mandibula'),
        ('6','Lengua'),
        ('7','Paladar'),
        ('8','Piso de boca'),
        ('9','Orofaringe'),
        ('10','Atm'),
        ('11','Ganglios'),
        ('12','Carillos'),
    )
    id_atencion = models.ForeignKey(Atencion, models.DO_NOTHING, db_column='id_atencion', blank=True, null=True)
    tipo = models.CharField('Tipos',max_length=5, choices = selector)
    detalle = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'estomatogmatico'


class PlanesDiagnostico(models.Model):
    id_atencion = models.ForeignKey(Atencion, models.DO_NOTHING, db_column='id_atencion', blank=True, null=True)
    procedimiento = models.TextField(blank=True, null=True)
    detalles = models.TextField(blank=True, null=True)
    tipo = models.TextField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'planes_diagnostico'


class SaludOral(models.Model):
    id_atencion = models.ForeignKey(Atencion, models.DO_NOTHING, db_column='id_atencion', blank=True, null=True)
    piezas_dentales = models.IntegerField(blank=True, null=True)
    placa = models.IntegerField(blank=True, null=True)
    calculo = models.IntegerField(blank=True, null=True)
    gingivitis = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'salud_oral'

class SignosVitales(models.Model):
    id_atencion = models.ForeignKey(Atencion, models.DO_NOTHING, db_column='id_atencion', blank=True, null=True)
    presion_arterial = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    frecuencia_cardiaca = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    temperatura = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    frecuencia_respiratoria = models.DecimalField(max_digits=4, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'signos_vitales'