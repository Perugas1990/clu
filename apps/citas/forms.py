from django import forms

from .models import Agenda

import datetime

from apps.cliente.models import Usuario

class CitaUpdateForm(forms.ModelForm):
    
    comentario = forms.CharField(widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):   
        super(CitaUpdateForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if not isinstance(field, forms.BooleanField):
                field.widget.attrs['class'] = 'form-control'

        self.fields['fecha_desde'].widget.attrs['class'] = 'form-control flatpickr-date-time flatpickr-input active'
        self.fields['fecha_hasta'].widget.attrs['class'] = 'form-control flatpickr-date-time flatpickr-input active' 
        self.fields["comentario"].widget.attrs['rows'] = 3
        

    class Meta:
        model = Agenda
        fields = [
            'fecha_desde',
            'fecha_hasta',
            'comentario',

        ]