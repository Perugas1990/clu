from django.urls import path, re_path
from .views import citas_agregar_views, agendar_create_view1, citas_list_view, all_events, CalendarioListView
from django.contrib.auth.decorators import login_required

app_name = 'citas'

urlpatterns = [
    path(
        'agregar/', 
        agendar_create_view1,
        name = 'agregar_citas'
    ),
    path(
        'editar/<int:id>/', 
        login_required(agendar_create_view1),
        name='confirmar_cita'
    ),
    path(
        'listar/', 
        login_required(citas_list_view),
        name='listar_cita'
    ),
    path(
        'calendario/', 
        login_required(CalendarioListView.as_view()),
        name='calendario'
    ),
    re_path('^all_events', all_events, name='all_events'),
]
