from django.shortcuts import render
from django.views.generic import (
    TemplateView,
)

# Create your views here.

def citas_agregar_views(request):
    template_name = 'calendario.html'
    context = {}
    return render(request, template_name, context)
