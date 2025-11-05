from django.contrib import admin

# Register your models here.
from .models import Time, Partida #importa nossos modelos

# Registra os modelos para que apareçam na área de administração
admin.site.register(Time)
admin.site.register(Partida)