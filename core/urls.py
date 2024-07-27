from django.urls import path
from .views import( listar_continentes, detalhar_continente, adicionar_continente,
    listar_patrias, detalhar_patria, adicionar_patria, listar_estados, detalhar_estado,
    adicionar_estado, listar_cidades, detalhar_cidade, adicionar_cidade)
    

urlpatterns = [
    path('', listar_continentes, name='listar_continentes'),
    path('continente/<int:id>/', detalhar_continente, name='detalhar_continente'),
	path('adicionar/', adicionar_continente, name='adicionar_continente'),
    path('patrias/', listar_patrias, name='listar_patrias'),
    path('patria/<int:id>/', detalhar_patria, name='detalhar_patria'),
	path('adicionar/', adicionar_patria, name='adicionar_patria'),
    path('estados/', listar_estados, name='listar_estados'),
    path('estado/<int:id>/', detalhar_estado, name='detalhar_estado'),
	path('adicionar/', adicionar_estado, name='adicionar_estado'),
    path('cidades/', listar_cidades, name='listar_cidades'),
    path('cidade/<int:id>/', detalhar_cidade, name='detalhar_cidade'),
	path('adicionar/', adicionar_cidade, name='adicionar_cidade'),
    
]    