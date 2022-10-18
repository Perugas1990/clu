from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CitaUpdateForm
from django.views.generic import (
    TemplateView,
)

# Create your views here.
@login_required(login_url='/')
def citas_agregar_views(request):
    template_name = 'calendario.html'
    context = {}
    return render(request, template_name, context)

@login_required
def agendar_create_view1(request, id=None):
    template_name = 'agendar_cita.html'

    cliente_id = request.user.id
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
                cliente = request.user.id
                fecha_desde = form.cleaned_data.get('fecha_desde')
                fecha_hasta = form.cleaned_data.get('fecha_hasta')
                comentario = form.cleaned_data.get('comentario')
                estado = form.cleaned_data.get('estado')

                citas = Agenda.objects.create(
                    cliente = cliente,
                    empresa = empresa,
                    fecha_desde = fecha_desde,
                    fecha_hasta = fecha_hasta,
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
