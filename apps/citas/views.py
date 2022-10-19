from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from .forms import CitaUpdateForm
from django.core.paginator import Paginator
from django.views.generic import (
    TemplateView,
    ListView,
)
from .models import Agenda
from apps.cliente.models import Usuario
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import json

# Create your views here.
@login_required(login_url='/')
def citas_agregar_views(request):
    template_name = 'calendario.html'
    context = {}
    return render(request, template_name, context)

class CalendarioListView(ListView):
    model = Agenda
    template_name = 'calendario.html'
    context_object_name = 'agenda'

    def get_queryset(self):
        cliente_id = self.request.user.id
        return Agenda.objects.filter(cliente=cliente_id)

@login_required
def agendar_create_view1(request, id=None):
    template_name = 'agendar_cita.html'

    #cliente_id = request.user.id
    cliente = Usuario.objects.get(id=int(request.user.id))
    #Empresa.objects.get(razon_social=request.session['empresa_name'])
    #print(cliente_id)
    if id:
        agenda_medica = get_object_or_404(Agenda, pk=id)
        estado_boton=agenda_medica.estado
        form = CitaUpdateForm(request.POST or None, instance = agenda_medica)

    else:
        form = CitaUpdateForm(request.POST or None)
        estado_boton=None

    if request.method == 'POST':

        if form.is_valid():

            if 'btn_agregar_agenda' in request.POST:
                fecha = form.cleaned_data.get('fecha')
                desde = form.cleaned_data.get('desde')
                hasta = form.cleaned_data.get('hasta')
                comentario = form.cleaned_data.get('comentario')
                estado = form.cleaned_data.get('estado')

                citas = Agenda.objects.create(
                    cliente = cliente,
                    fecha = fecha,
                    desde = desde,
                    hasta = hasta,
                    comentario = comentario,
                    estado = 'BORRADOR',
                    
                )
                citas.save()

                return redirect('citas:confirmar_cita', id=citas.id)

            if 'btn_confirmar_agenda' in request.POST:
                form_agenda = form.save(commit=False)
                form_agenda.estado = 'CONFIRMADO'
                form_agenda.save()

                return redirect('citas:listar_cita')

            if 'btn_cancelar_agenda' in request.POST:
                form_agenda = form.save(commit=False)
                form_agenda.estado = 'CANCELADA'
                form_agenda.save()

                return redirect('citas:listar_cita')
            
            if 'btn_atender_agenda' in request.POST:
                form_agenda = form.save(commit=False)
                form_agenda.estado = 'ATENDIDA'
                form_agenda.save()

                return redirect('citas:listar_cita')

    context = {
        'form':form,
        'id':id,
        'estado_boton':estado_boton,
    }
    return render(request, template_name, context)

def citas_list_view(request):
    
    cliente_id = request.user.id
    query = request.GET.get('busqueda',None)

    if query is not None:
        agenda = Agenda.objects.filter(Q(empresa__id=empresa_id),Q(cliente__razon_social_comprador__icontains=query)).order_by('fecha_desde')
        
    else:
        agenda = Agenda.objects.filter(cliente=cliente_id).order_by('fecha')
    
    p = Paginator(agenda, 5)
    template_name = 'listar_cita.html' 
    

    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)  
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)

    context = {
        'page_obj': page_obj,
        
    }
    return render(request, template_name, context)



# Display all events.
def all_events(request):  
    cliente_id = request.user.id
    all_events = Agenda.objects.filter(cliente=cliente_id) 
                                                                                    
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