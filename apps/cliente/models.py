from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Usuario(models.Model):
    opciones_genero = (
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino'),
        ('N/A', 'N/A'),
    )
    tipos_sangre = (
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
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
        ('11','11'),
        ('12','12'),
        ('13','13'),
        ('14','14'),
        ('15','15'),
        ('16','16'),
        ('17','17'),
        ('18','18'),
        ('21','21'),
        ('22','22'),
        ('23','23'),
        ('24','24'),
        ('25','25'),
        ('26','26'),
        ('27','27'),
        ('28','28'),
        ('31','31'),
        ('32','32'),
        ('33','33'),
        ('34','34'),
        ('35','35'),
        ('36','36'),
        ('37','37'),
        ('38','38'),
        ('41','41'),
        ('42','42'),
        ('43','43'),
        ('44','44'),
        ('45','45'),
        ('46','46'),
        ('47','47'),
        ('48','48'),
        ('51','51'),
        ('52','52'),
        ('53','53'),
        ('54','54'),
        ('55','55'),
        ('61','61'),
        ('62','62'),
        ('63','63'),
        ('64','64'),
        ('65','65'),
        ('71','71'),
        ('72','72'),
        ('73','73'),
        ('74','74'),
        ('75','75'),
        ('81','81'),
        ('82','82'),
        ('83','83'),
        ('84','84'),
        ('85','85'),
    )
    simbologia = (
        ('Sellante necesario','Sellante necesario'),
        ('A-Sellante necesario','A-Sellante necesario'),
        ('Extraccion indicada','Extraccion indicada'),
        ('Perdida por caries','Perdida por caries'),
        ('Perdida(otra causa)','Perdida(otra causa)'),
        ('Endodoncia','Endodoncia'),
        ('Protesis Fija','Protesis Fija'),
        ('Protesis removible','Protesis removible'),
        ('Protesis total','Protesis total'),
        ('Corona','Corona'),
        ('Caries','Caries'),
        ('Obturado','Obturado'),
    )
    id_atencion = models.ForeignKey(Atencion, models.DO_NOTHING, db_column='id_atencion', blank=True, null=True)
    diente = models.CharField('Tipos',max_length=5, choices = selector)
    detalle = models.CharField('Simbologia',max_length=35, choices = simbologia)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'odontograma'




class Estomatogmatico(models.Model):

    selector = (
        ('Labios','Labios'),
        ('Glandulas salivales','Glandulas salivales'),
        ('Mejilla','Mejilla'),
        ('Maxilar','Maxilar'),
        ('Mandibula','Mandibula'),
        ('Lengua','Lengua'),
        ('Paladar','Paladar'),
        ('Piso de boca','Piso de boca'),
        ('Orofaringe','Orofaringe'),
        ('Atm','Atm'),
        ('Ganglios','Ganglios'),
        ('Carillos','Carillos'),
    )
    id_atencion = models.ForeignKey(Atencion, models.DO_NOTHING, db_column='id_atencion', blank=True, null=True)
    tipo = models.CharField('Tipos',max_length=45, choices = selector)
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
    presion_arterial = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    frecuencia_cardiaca = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    temperatura = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    frecuencia_respiratoria = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'signos_vitales'