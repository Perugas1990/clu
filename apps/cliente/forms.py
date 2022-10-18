from django import forms

from django.contrib.admin import widgets

from .models import Usuario
from datetime import datetime, date

class UpdateClienteForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super(UpdateClienteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'
        
        self.fields['fecha_nacimiento'].widget.attrs['class'] = 'form-control mydatepicker'
        
    
    class Meta:
        model = Usuario
        fields = [
            'identificacion',
            'nombres',
            'apellidos',
            'lugar_nacimiento',
            'fecha_nacimiento',
            'edad',
            'direccion',
            'canton',
            'provincia',
            'pais',
            'sexo',
            'tipo_sangre',
            'celular',
            'correo',
            #Contacto emergencia
            'nombre_contacto_emergencia',
            'parentesco_contacto_emergencia',
            'telefono_contacto_emergencia',
            #Menor de Edad
            'is_menor',
            'nombre_tutor',
            'parentesco_tutor',
            'telefono_tutor',
            'direccion_tutor',
        ]
        