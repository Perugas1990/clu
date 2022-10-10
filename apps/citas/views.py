from django.shortcuts import render
from django.views.generic import (
    TemplateView,
)

# Create your views here.

class citas_agregar_views(TemplateView):
    template_name = 'home.html'