from django.urls import path, re_path
from .views import citas_agregar_views, agendar_create_view1

app_name = 'citas'

urlpatterns = [
    path(
        'agregar/', 
        agendar_create_view1,
        name = 'agregar_citas'
    ),
]
