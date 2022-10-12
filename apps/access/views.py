from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from apps.cliente.models import Usuario
@login_required
def home_view(request):
    template_name = 'home.html'
    context = {}
    return render(request, template_name, context)