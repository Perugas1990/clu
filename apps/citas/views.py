from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    TemplateView,
)

# Create your views here.
@login_required(login_url='/')
def citas_agregar_views(request):
    template_name = 'calendario.html'
    context = {}
    return render(request, template_name, context)
