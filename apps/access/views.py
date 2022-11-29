from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.cliente.models import Usuario
from .models import Empresa, Medico
from .forms import EmpresaClienteForm, ContactoClienteForm
from django.urls import reverse_lazy, reverse

from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
)


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

class EmpresaUpdateView(UpdateView):
    model = Empresa
    template_name = 'editar_empresa.html'
    form_class = EmpresaClienteForm

    def get_success_url(self):
        usuario_id = self.request.user.id
        return reverse('cliente:ver_cliente', kwargs={'pk': usuario_id})

class ContactoUpdateView(UpdateView):
    model = Medico
    template_name = 'editar_contacto.html'
    form_class = ContactoClienteForm

    def get_success_url(self):
        usuario_id = self.request.user.id
        return reverse('cliente:ver_cliente', kwargs={'pk': usuario_id})