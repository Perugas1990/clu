from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.cliente.models import Usuario
from .models import Empresa, Medico


def home_view(request):
    template_name = 'home.html'
    empresa=Empresa.objects.get(pk=1)
    medico=Medico.objects.get(pk=1)
    print('probando')
    print(empresa.nombre)
    context = {
        'empresa' : empresa,
        'medico' : medico,
    }
    return render(request, template_name, context)

def mision_view(request):
    template_name = 'mision.html'
    empresa=Empresa.objects.get(pk=1)
    medico=Medico.objects.get(pk=1)
    print('probando')
    print(empresa.nombre)
    context = {
        'empresa' : empresa,
        'medico' : medico,
    }
    return render(request, template_name, context)