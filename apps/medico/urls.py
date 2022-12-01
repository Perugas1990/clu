from django.urls import path, re_path
from .views import (
    historial_list_view, export_recetario_medico,
    atencion_view, InsumosCreateView, InsumosListView, 
    CalendarioMedicoListView, all_events1, UsuarioListView, 
    CitasMedicoListView, ProveedorCreateView, crear_insumo
    )
from django.contrib.auth.decorators import login_required


app_name = 'medico'

urlpatterns = [
    path(
        'registrar/proveedor/', 
        login_required(ProveedorCreateView.as_view()),
        name='registrar_proveedor'
    ),
    path(
        'crear/insumos/', 
        login_required(crear_insumo),
        name='crear_insumos'
    ),
    path(
        'listar/insumos/', 
        login_required(InsumosListView.as_view()),
        name='listar_insumos'
    ),
    path(
        'calendario/', 
        login_required(CalendarioMedicoListView.as_view()),
        name='calendario_medico'
    ),
    path(
        'clientes/', 
        login_required(UsuarioListView.as_view()),
        name='clientes_medico'
    ),
    path(
        'citas_cliente/<id>/', 
        login_required(CitasMedicoListView.as_view()),
        name='citas_cliente_medico'
    ),
    path(
        'atencion_cliente/<id>/', 
        login_required(atencion_view),
        name='crear_atencion'
    ),
    path(
        'list_historial/<id>/', 
        login_required(historial_list_view),
        name='list_historial'
    ),
    path('print/recetario/<int:id>/<int:atencion>/', export_recetario_medico, name='print_recetario'),
    re_path('^all_events', all_events1, name='all_events'),
]