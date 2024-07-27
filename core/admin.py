from django.contrib import admin

from .models import(
    Continente, Patrias, Estados, Cidades
)

admin.site.register(Continente)
admin.site.register(Patrias)
admin.site.register(Estados)
admin.site.register(Cidades)


class ContinenteAdmin(admin.ModelAdmin):
    list_display = (
        'nome'
    )

class PatriasAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'capital'
    )

class EstadosAdmin(admin.ModelAdmin):
    list_display = (
        'nome'
    )

class CidadesAdmin(admin.ModelAdmin):
    list_display = (
        'nome'
    )




