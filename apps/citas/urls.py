from django.urls import path, re_path
from .views import citas_agregar_views

app_name = 'citas'

urlpatterns = [
    path(
        'agregar/', 
        citas_agregar_views.as_view(),
        name = 'agregar_citas'
    ),
]
