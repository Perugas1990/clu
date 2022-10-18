from django.urls import path, re_path
from .views import VerPerfilUsuario, signup, login_view, logout_view, ClienteUpdateView
from django.contrib.auth.decorators import login_required

app_name = 'cliente'

urlpatterns = [
    path(
        'signup/', 
        signup,
        name='signup'
    ),
    path(
        '', 
        login_view,
        name='login'
    ),
    path(
        'logout/', 
        logout_view,
        name='logout'
    ),
    path(
        'ver/<pk>/', 
        login_required(VerPerfilUsuario.as_view()),
        name='ver_cliente'
    ),
    path(
        'editar/<pk>/', 
        login_required(ClienteUpdateView.as_view()),
        name='editar_cliente'
    ),
]
