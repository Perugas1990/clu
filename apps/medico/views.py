from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import Insumos
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
)

# Create your views here.
class InsumosCreateView(CreateView):
    model = Insumos 
    template_name = 'crear_insumo.html'
    fields = ['nombre', 'detalle', 'stock']
    success_url = reverse_lazy('citas:agregar_citas')