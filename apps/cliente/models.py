from django.db import models

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

    def __str__(self):
        return self.nombres + ' ' + self.apellidos

    class Meta:
        managed = False
        db_table = 'usuario'
