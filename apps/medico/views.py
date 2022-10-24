from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy, reverse
from .models import Insumos
from apps.citas.models import Agenda
from apps.cliente.models import Usuario
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
)

from django.http import HttpResponse, JsonResponse
import json

# Create your views here.
class InsumosCreateView(CreateView):
    model = Insumos 
    template_name = 'crear_insumo.html'
    fields = ['nombre', 'detalle', 'stock']
    success_url = reverse_lazy('medico:agregar_insumos')

class InsumosListView(ListView):
    model = Insumos
    template_name = 'listar_insumos.html'
    context_object_name = 'insumos'

class UsuarioListView(ListView):
    model = Usuario
    template_name = 'clientes_medico/listar_clientes.html'
    context_object_name = 'clientes'
    paginate_by = 25

class CalendarioMedicoListView(ListView):
    model = Agenda
    template_name = 'cita_medica/calendario.html'
    context_object_name = 'agenda'

def all_events1(request, id = None):  
    
    all_events = Agenda.objects.all() 
                                                                                    
    out = []                                                                                                             
    for event in all_events:  
        if event.estado == "CANCELADA":
            color = 'rgb(255,51,51)'
        elif event.estado == "CONFIRMADO":
            color = 'rgb(136,255,77)'
        elif event.estado == "BORRADOR":
            color = 'grey'
        else:
            color = 'rgb(153, 204, 255)'  
        fecha_desde = event.fecha.strftime("%Y-%m-%d")+event.desde.strftime("T%H:%M:%S")
        fecha_hasta = event.fecha.strftime("%Y-%m-%d")+event.hasta.strftime("T%H:%M:%S")                                                                                       
        out.append({                                                                                                    
            'title': event.comentario,                                                                                         
            'id': event.id,                                                                                              
            'start': fecha_desde,                                                         
            'end': fecha_hasta,
            'backgroundColor': color,
            'borderColor': color, 
            'textColor': 'white'
            })  

                                                          
    
    return JsonResponse(out, safe=False)

class CitasMedicoListView(ListView):
    model = Agenda
    template_name = 'cita_medica/listar_cita.html'
    context_object_name = 'agenda'
    def get_queryset(self):
        id = self.kwargs['id']
        agenda = Agenda.objects.filter(cliente=id)
        return agenda