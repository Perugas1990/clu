from django import forms

from django.contrib.admin import widgets

from .models import Empresa, Medico
from datetime import datetime, date

class EmpresaClienteForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super(EmpresaClienteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'     
     
    class Meta:
        model = Empresa
        fields = [
            'nombre',
            'mision',
            'vision',
            'direccion',
            'id_empresa',
        ]


class ContactoClienteForm(forms.ModelForm):
    
    
    def __init__(self, *args, **kwargs):
        super(ContactoClienteForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'     
     
    class Meta:
        model = Medico
        fields = [
            'nombres',
            'apellidos',
            'cedula_field',
            'correo',
            'telefono',
        ]

    