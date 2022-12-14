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
        self.fields["comentario"].widget.attrs['rows'] = 3
        self.fields['fecha'].widget.attrs['class'] = 'form-control flatpickr-basic flatpickr-input'
        self.fields['desde'].widget.attrs['class'] = 'form-control flatpickr-time text-start flatpickr-input active'
        self.fields['hasta'].widget.attrs['class'] = 'form-control flatpickr-time text-start flatpickr-input active'
        

    class Meta:
        model = Agenda
        fields = [
            'fecha',
            'desde',
            'hasta',
            'comentario',

        ]