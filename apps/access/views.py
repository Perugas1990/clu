from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def home_view(request):
    
    template_name = 'base.html'
    context = {}
    return render(request, template_name, context)