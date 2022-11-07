from django import forms

from django.contrib.admin import widgets

from apps.cliente.models import Usuario, Atencion, Historial, Estomatogmatico, SignosVitales, Odontograma, PlanesDiagnostico
from datetime import datetime, date



class AtencionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AtencionForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Atencion
        fields = [
            'm_consulta', 
            'enf_actual',
            'antecedentes',        
        ]

class EstomatogmaticoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EstomatogmaticoForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Estomatogmatico
        fields = [
            'tipo', 
            'detalle',        
        ]

class SignosForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SignosForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = SignosVitales
        fields = [
            'presion_arterial', 
            'frecuencia_cardiaca',    
            'temperatura',   
            'frecuencia_respiratoria',
        ]

class OdontogramaForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(OdontogramaForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'
    class Meta:
        model = Odontograma
        fields = [
            'diente', 
            'detalle',    
        ]
