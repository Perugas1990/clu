from django.urls import path, re_path
from .views import InsumosCreateView
from django.contrib.auth.decorators import login_required


app_name = 'medico'

urlpatterns = [
    path(
        'crear/insumos/', 
        login_required(InsumosCreateView.as_view()),
        name='crear_insumos'
    ),
]