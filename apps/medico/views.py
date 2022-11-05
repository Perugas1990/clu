from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy, reverse
from .models import Insumos
from apps.citas.models import Agenda
from apps.cliente.models import Usuario, Atencion, Historial, Estomatogmatico
from .forms import AtencionForm, EstomatogmaticoForm
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
    
def atencion_view(request,id=None):
    template_name = 'agenda/crear_atencion.html'
    form_atencion = AtencionForm(request.POST or None)
    form_estomatogmatico = EstomatogmaticoForm(request.POST or None)
    usuario = Usuario.objects.get(id=id)
    historial_id = Historial.objects.get(cliente = usuario)
    print(historial_id.id)
    if request.method == 'POST':

        if form_atencion.is_valid():

            consulta = form_atencion.cleaned_data.get('m_consulta')
            enfermedad = form_atencion.cleaned_data.get('enf_actual')
            antecedentes = form_atencion.cleaned_data.get('antecedentes')

            atencion = Atencion.objects.create(
                m_consulta = consulta,
                enf_actual = enfermedad,
                antecedentes = antecedentes,
                id_historial = historial_id,
            )            
            atencion.save()
            if form_estomatogmatico.is_valid():

                atencion_id = Atencion.objects.get(id=atencion.id)
                tipo = form_estomatogmatico.cleaned_data.get('tipo')
                detalle = form_estomatogmatico.cleaned_data.get('detalle')

                atencion = Estomatogmatico.objects.create(
                    id_atencion=atencion_id,
                    tipo = consulta,
                    detalle = enfermedad,
                )
                if form_estomatogmatico.is_valid():

                    atencion_id = Atencion.objects.get(id=atencion.id)
                    tipo = form_estomatogmatico.cleaned_data.get('tipo')
                    detalle = form_estomatogmatico.cleaned_data.get('detalle')

                    atencion = Estomatogmatico.objects.create(
                        id_atencion=atencion_id,
                        tipo = consulta,
                        detalle = enfermedad,
                    )

                    return redirect('medico:clientes_medico')

    context = {
        'atencion':form_atencion,
        'estomatogmatico': form_estomatogmatico, 

    }
    
    return render(request, template_name, context)


def estomatogmatico_view(request,id=None):
    template_name = 'agenda/crear_estomatogmatico.html'
    form = EstomatogmaticoForm(request.POST or None)
    atencion_id = id
    print(historial_id.id)
    if request.method == 'POST':

        if form.is_valid():

            tipo = form.cleaned_data.get('tipo')
            detalle = form.cleaned_data.get('detalle')

            atencion = Atencion.objects.create(
                tipo = consulta,
                detalle = enfermedad,
            )
            atencion.save()
            return redirect('medico:clientes_medico')

    context = {
        'form':form,

    }
    
    return render(request, template_name, context)