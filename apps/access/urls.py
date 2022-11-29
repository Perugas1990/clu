from django.urls import path, re_path
from .views import home_view, mision_view

app_name = 'access'

urlpatterns = [
    path('',home_view,name = 'home'),
    path('mision/', mision_view, name = 'mision'),
]
