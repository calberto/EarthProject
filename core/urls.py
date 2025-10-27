from django.urls import path
from .views import( listar_continentes, detalhar_continente, continente_delete_confirm, salvar_continente,
    listar_patrias, detalhar_patria,  listar_estados, detalhar_estado, listar_cidades, detalhar_cidade,home,
    salvar_cidade, salvar_estado, salvar_patria, cidade_delete_confirm, estado_delete_confirm,
    patria_delete_confirm, executar_script, atualizar_dados, home_continente,novo_continente, NewContinenteForm)
# from .atualiza import fetch_population_data,update_population_from_dataframe


# app_name = 'core'

urlpatterns = [
    path('', home, name='core_home'),

    path('listar_continentes/', listar_continentes, name='core_listar_continentes'),
    path('detalhar_continente/<int:continente_id>/', detalhar_continente, name='sistema_detalhar_continente'),
    path('salvar_continente/', salvar_continente, name='core_salvar_continente'),
    path('continente_delete_confirm/<int:continente_pk>/', continente_delete_confirm, name='core_continente_delete_confirm'),
    path('continente/', home_continente, name='home_continente'),
	#path('newcontinente/', newcontinente_popup, name='newcontinente_popup'),
    path('novo_continente/', novo_continente, name='core_novo_continente'),


    path('listar_cidades/', listar_cidades, name='core_listar_cidades'),
    path('detalhar_cidade/<int:cidade_id>/', detalhar_cidade, name='sistema_detalhar_cidade'),
    path('salvar_cidade/', salvar_cidade, name='core_salvar_cidade'),
    path('cidade_delete/<int:cidade_pk>/', cidade_delete_confirm, name='core_cidade_delete_confirm'),

    path('listar_estados/', listar_estados, name='core_listar_estados'),
    path('detalhar_estado/<int:estado_id>/', detalhar_estado, name='sistema_detalhar_estado'),
    path('salvar_estado/', salvar_estado, name='core_salvar_estado'),
    path('estado_delete/<int:estado_pk>/', estado_delete_confirm, name='core_estado_delete_confirm'),

    # path('listar_patrias/', listar_patrias, name='core_listar_patrias'),
    path('detalhar_patria/<int:patria_id>/', detalhar_patria, name='sistema_detalhar_patria'),
    path('salvar_patria/', salvar_patria, name='core_salvar_patria'),
    path('patria_delete/<int:patria_pk>/', patria_delete_confirm, name='core_patria_delete_confirm'),

    path("executar-script/", executar_script, name="core_executar_script"),
    # path('atualizar-patrias/', atualizar_patrias, name='core_atualizar_patrias'),
    path('listar_patrias/', listar_patrias, name='core_listar_patrias'),
    path('update_population_from_dataframe/', atualizar_dados, name='core_update_population_from_dataframe'),



    # path('export-csv/', export_to_csv, name='export_to_csv'),
    # path('export-pdf/', export_to_pdf, name='export_to_pdf'),

]
