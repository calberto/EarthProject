from django.contrib import admin

from .models import(
    Continentes, Cidades, Estados, Patrias
)

admin.site.register(Continentes), 
admin.site.register(Cidades), 
admin.site.register(Estados), 
admin.site.register(Patrias)

class ContinenteAdmin(admin.ModelAdmin):
    list_display = {
        "nome"
    }

class CidadeAdmin(admin.ModelAdmin):
    list_display = {
        "nome"
    }

class EstadoAdmin(admin.ModelAdmin):
    list_display = {
        "nome"
    }

class PatriaAdmin(admin.ModelAdmin):
    list_display = ('nome','capital')
