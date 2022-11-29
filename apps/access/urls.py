from django.urls import path, re_path
from .views import home_view, mision_view, EmpresaUpdateView, ContactoUpdateView
from django.contrib.auth.decorators import login_required

app_name = 'access'

urlpatterns = [
    path('',home_view,name = 'home'),
    path('mision/', mision_view, name = 'mision'),
    path(
        'editar/empresa/<pk>/', 
        login_required(EmpresaUpdateView.as_view()),
        name='editar_empresa'
    ),
    path(
        'editar/contacto/<pk>/', 
        login_required(ContactoUpdateView.as_view()),
        name='editar_contacto'
    ),
]
