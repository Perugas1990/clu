from datetime import datetime, timedelta, date
from django.shortcuts import get_object_or_404, redirect, render
from django.http.response import Http404, HttpResponse
from django.contrib.auth.decorators import permission_required
from django.urls import reverse_lazy, reverse
from .models import Insumos, Proveedor, Producto
from django.db.models import Q
from apps.citas.models import Agenda
from apps.cliente.models import Usuario, Atencion, Historial, Estomatogmatico, SignosVitales, Odontograma
from .forms import AtencionForm, EstomatogmaticoForm, SignosForm, OdontogramaForm, ProductoForm
from .parsers import export_reporte_hoja_calculo
from .constantes import FORMATOS_ARCHIVOS
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
)

from django.http import HttpResponse, JsonResponse
import json

# Create your views here.

class ProveedorCreateView(CreateView):
    model = Proveedor
    template_name = 'registrar_proveedor.html'
    fields = [
        'identificacion', 
        'nombre', 
        'apellido',
        'telefono',
        'direccion',
        'correo'
        ]

    success_url = reverse_lazy('medico:registrar_proveedor')

class InsumosCreateView(CreateView):
    model = Insumos 
    template_name = 'crear_insumo.html'
    fields = ['nombre', 'detalle', 'stock']
    success_url = reverse_lazy('medico:agregar_insumos')

def crear_insumo(request):
    template_name = 'crear_insumo.html'
    producto=ProductoForm(request.POST or None)
    context = {
        'producto':producto
    }
    if request.method == 'POST':
        if producto.is_valid():
            nombre = producto.cleaned_data.get('nombre')
            precio = producto.cleaned_data.get('precio')
            cantidad = producto.cleaned_data.get('cantidad')
            id_proveedor = producto.cleaned_data.get('id_proveedor')
            total = precio*cantidad

            producto_obj = Producto.objects.create(
                nombre = nombre,
                precio = precio,
                cantidad = cantidad,
                total = total,
                id_proveedor = id_proveedor,                        
                )
            try:
                insumo = Insumos.objects.get(id_producto=producto_obj.id)
            except:
                producto_id=Producto.objects.get(id=producto_obj.id)
                Insumos.objects.create(
                    id_producto=producto_id,
                    cantidad=cantidad,
                )
            
            #producto.save()
            
            return redirect('cliente:editar_cliente', request.user.id)



    return render(request, template_name, context)
    

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
    form_signos = SignosForm(request.POST or None)
    print(form_signos)
    form_odontograma = OdontogramaForm(request.POST or None)
    usuario = Usuario.objects.get(id=id)
    historial_id = Historial.objects.get(cliente = usuario)
    print(historial_id.id)
    if request.method == 'POST':

        if form_atencion.is_valid():
            print('atencion')
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
            if form_signos.is_valid():
                print('signos')
                atencion_id = Atencion.objects.get(id=atencion.id)
                presion_arterial = form_signos.cleaned_data.get('presion_arterial')
                frecuencia_cardiaca = form_signos.cleaned_data.get('frecuencia_cardiaca')
                temperatura = form_signos.cleaned_data.get('temperatura')
                frecuencia_respiratoria = form_signos.cleaned_data.get('frecuencia_respiratoria')

                signos = SignosVitales.objects.create(
                    id_atencion=atencion_id,
                    presion_arterial = presion_arterial,
                    frecuencia_cardiaca = frecuencia_cardiaca,
                    temperatura = temperatura,
                    frecuencia_respiratoria = frecuencia_respiratoria,
                )
                signos.save()
                if form_estomatogmatico.is_valid():
                    print('estomatogmatico')
                    tipo = form_estomatogmatico.cleaned_data.get('tipo')
                    detalle = form_estomatogmatico.cleaned_data.get('detalle')

                    estomatogmatico = Estomatogmatico.objects.create(
                        id_atencion=atencion_id,
                        tipo = tipo,
                        detalle = detalle,
                    )
                    estomatogmatico.save()
                    if form_odontograma.is_valid():
                        print('odontograma')
                        diente= form_odontograma.cleaned_data.get('diente')
                        detalle = form_odontograma.cleaned_data.get('detalle')

                        odontograma = Odontograma.objects.create(
                            id_atencion=atencion_id,
                            diente = diente,
                            detalle = detalle,
                        )
                        odontograma.save()

                    return redirect('medico:clientes_medico')

    context = {
        'atencion':form_atencion,
        'estomatogmatico': form_estomatogmatico, 
        'signos': form_signos, 
        'odontograma' : form_odontograma,

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

def export_recetario_medico(request, id, atencion):
    """
    Exportar recetario medico
    """
    usuario = Usuario.objects.get(id=id)
    historial = get_object_or_404(Historial,cliente=usuario.pk)
    atencion = Atencion.objects.get(Q(id_historial=historial.pk),Q(id=atencion))
    signos = get_object_or_404(SignosVitales,id_atencion=atencion.pk)
    estomatogmatico = get_object_or_404(Estomatogmatico,id_atencion=atencion.pk)
    odontograma = get_object_or_404(Odontograma,id_atencion=atencion.pk)
    print(atencion.pk)
    print(usuario.pk)
    plantilla = 'recetario.odt'

    template_recetario = 'apps/medico/receta/templates/odt/' + plantilla

    template_documento = template_recetario

    
    content_type = FORMATOS_ARCHIVOS.get('PDF').get('content_type')

    now = datetime.now()
    dia = now.day
    mes = now.month
    año = now.year

    data = {
        'u':usuario,
        'd':dia,
        'm':mes,
        'a':año,
        'at': atencion,
        's': signos,
        'es': estomatogmatico,
        'o' :odontograma,
    }

    archivo_salida = export_reporte_hoja_calculo(
        data, template_documento, 'PDF'
    )

    with open(archivo_salida, 'rb') as archivo_salida:
        response = HttpResponse(archivo_salida.read(),
                                content_type=content_type)
        response['Content-Disposition'] = 'inline; filename=RM-{0}.pdf'
        
    return response

class HistorialListView(ListView):
    model = Atencion
    template_name = 'agenda/list_atencion.html'
    context_object_name = 'atencion'
    def get_queryset(self):
        id = self.kwargs['id']
        usuario = Usuario.objects.get(id=id)
        historial = get_object_or_404(Historial,cliente=usuario.pk)
        atencion = Atencion.objects.filter(id_historial=historial.pk)
        return atencion

    def get_context_data(self,**kwargs):
        context = super(HistorialListView,self).get_context_data(**kwargs)
        id = self.kwargs['id']
        usuario = Usuario.objects.get(id=id)
        context['usuario']=usuario.pk
        return context

def historial_list_view(request, id):
    usuario = Usuario.objects.get(id=id)
    historial = get_object_or_404(Historial,cliente=usuario.pk)
    atencion = Atencion.objects.filter(id_historial=historial.pk)
    template_name = 'agenda/list_atencion.html'

    context = {
        'atencion':atencion,
        'usuario':usuario.pk,
        
    }
    return render(request, template_name, context)