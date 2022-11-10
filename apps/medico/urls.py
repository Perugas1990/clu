from django.urls import path, re_path
from .views import export_recetario_medico,atencion_view, InsumosCreateView, InsumosListView, CalendarioMedicoListView, all_events1, UsuarioListView, CitasMedicoListView
from django.contrib.auth.decorators import login_required


app_name = 'medico'

urlpatterns = [
    path(
        'crear/insumos/', 
        login_required(InsumosCreateView.as_view()),
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
    path('print/recetario/<int:id>/', export_recetario_medico, name='print_recetario'),
    re_path('^all_events', all_events1, name='all_events'),
]