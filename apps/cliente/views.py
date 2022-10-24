from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from .forms import UpdateClienteForm
from .models import Usuario

from .models import Usuario
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
)


class VerPerfilUsuario(DetailView):
    model = Usuario
    template_name = 'ver_usuario.html'

class ClienteUpdateView(UpdateView):
    model = Usuario
    template_name = 'editar_cliente.html'
    form_class = UpdateClienteForm

    def get_success_url(self):
        usuario_id = self.request.user.id
        return reverse('cliente:ver_cliente', kwargs={'pk': usuario_id})

# Create your views here.
def login_view(request):

    if request.method == 'POST':
        username = request.POST['usuario']
        password = request.POST['passwd']
        user=authenticate(request, username=username, password=password)
        print(user)
        if user:
            
            login(request,user)
            #return reverse('cliente:ver_cliente', request.user.id)
            return redirect('cliente:editar_cliente', request.user.id)
        else:
            return render(request,'login.html',{'error':'Passwords no coinciden'})
    return render(request,'login.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        passwd = request.POST['passwd']
        passwd_confirmation = request.POST['passwd_confirmation']
        if passwd != passwd_confirmation:
            print('error')
            return render(request, 'signup.html', {'error':'Passwords no coinciden'} )
        if Usuario.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error1':'Nombre de usuario ya registrado'} )

        user = User.objects.create(
            username=username,
            password=make_password(passwd),
            first_name=nombre,
            last_name=apellido,
            )
        perfil = Usuario(
            id=user.id,
            username=username,
            nombres=nombre,
            apellidos=apellido
            )
        print(perfil)
        perfil.save()
        return redirect('cliente:login')
    return render(request, 'signup.html')
    
@login_required
def logout_view(request):
    logout(request)
    return redirect('cliente:login')
