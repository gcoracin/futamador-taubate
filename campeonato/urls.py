from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_partidas, name='lista_partidas'),
]