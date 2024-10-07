from django.shortcuts import render
from .models import Contato

import pdb
def home(request):
    return render(request, 'website/index.html')

def servicos(request):
    return render(request, 'website/servicos.html')

def contato(request):
    # pdb.set_trace()
    try:
        contato = {}
        contato['email'] = request.POST.get('email')
        contato['nome'] = request.POST.get('nome')
        contato['sobrenome'] = request.POST.get('sobrenomme')
        contato['endereco'] = request.POST.get('endereco')
        contato['mensagem'] = request.POST.get('mensagem')
        contato['receber_noticias'] = True if request.POST.get('receber-noticias') == 'on' else False
        Contato.objects.create(**contato)
    except Exception as e:
        mensagem = str(e)
    else:
        mensagem = 'Contato realizado com sucesso!'

    return render(request, 'website/contato.html', {'mensagem': mensagem})
    

def planos(request):
    return render(request, 'website/planos.html')

def sobre(request):
    return render(request, 'website/sobre.html')
