from django.urls import path, include

from .views import(
	home, servicos,planos, sobre, contato
) 

urlpatterns = [
	path('', home, name='website_home'),
    path('servicos', servicos, name='website_servicos'),
    path('contato', contato, name='website_contato'),
    path('planos', planos, name='website_planos'),
    path('sobre', sobre, name='website_sobre'),

]