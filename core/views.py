from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Continente, Patrias, Estados, Cidades
from .forms import ContinenteForm, PatriaForm, EstadoForm, CidadeForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import imghdr
from django.http import HttpResponse
from django.core.paginator import Paginator

def home(request):
    context = {'mensagem' : 'Olá Ninho!'}
    return render(request, 'core/index.html', context)


# @login_required

def listar_continentes(request):
    continentes = Continente.objects.all()
    form = ContinenteForm()
    data = {'continentes': continentes, 'form': form}
    return render(request, 'core/listar_continentes.html', data)


def salvar_continente(request):
    
    if request.method == 'POST':
        continente_id = request.POST.get('continente_id')
        if continente_id:  # Edição de categoria existente
            continente = get_object_or_404(Continente, pk=continente_id)
            form = ContinenteForm(request.POST, request.FILES, instance=continente)
        else:  # Novo livro
            form = ContinenteForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('core_listar_continentes')  # Redireciona após salvar
    else:
        form = ContinenteForm()

    return render(request, 'continente_form.html', {'form': form})

def detalhar_continente(request, continente_id):
    continente = get_object_or_404(Continente, pk=continente_id)
    data = {
        'nome': continente.nome,
        'versao': continente.versao,
        'created_at': continente.created_at,
        'updated_at': continente.updated_at,
        
    }
    return JsonResponse(data)

def continente_delete_confirm(request, continente_pk):
    continente = Continente.objects.get(pk=continente_pk)
    continente.delete()
    return redirect('core_listar_continentes')	

# Cidades
def listar_cidades(request):
    data = {}
    search = request.GET.get('search')
    if search:
        data['db'] = Cidades.objects.filter(nome__icontains=search)
    else:
        data['db'] = Cidades.objects.all()	

    
    # Configura o paginador: 10 itens por página
    paginator = Paginator(data['db'], 20)  # Mostra 10 estados por página

    # Obtém o número da página da URL
    pages = request.GET.get('page')

    data['db'] = paginator.get_page(pages)
    
    
    form = CidadeForm()
    data['form'] = form
    return render(request, 'core/listar_cidades.html', data)


def salvar_cidade(request):
    if request.method == 'POST':
        cidade_id = request.POST.get('cidade_id')
        if cidade_id:  # Edição de autor existente
            cidade = get_object_or_404(Cidades, pk=cidade_id)
            form = CidadeForm(request.POST, request.FILES, instance=cidade)
        else:  # Novo autor
            form = CidadeForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('core_listar_cidades')  # Redireciona após salvar
    else:
        form = CidadeForm()

    return render(request, 'cidade_form.html', {'form': form})

def detalhar_cidade(request, cidade_id):
    cidade = get_object_or_404(Cidades, pk=cidade_id)
    data = {
        'nome': cidade.nome,
        'versao': cidade.versao,
        'created_at': cidade.created_at,
        'updated_at': cidade.updated_at,
        'estados': cidade.estados.id if cidade.estados else None
        
    }
    return JsonResponse(data)

def cidade_delete_confirm(request, cidade_pk):
    cidade = Cidades.objects.get(pk=cidade_pk)
    cidade.delete()
    return redirect('core_listar_cidades')	

# Estados
def listar_estados(request):
    data = {}
    search = request.GET.get('search')
    if search:
        data['db'] = Estados.objects.filter(nome__icontains=search)
    else:
        data['db'] = Estados.objects.all()	

    
    # Configura o paginador: 10 itens por página
    paginator = Paginator(data['db'], 5)  # Mostra 10 estados por página

    # Obtém o número da página da URL
    pages = request.GET.get('page')

    data['db'] = paginator.get_page(pages)
    
    
    form = EstadoForm()
    data['form'] = form

    return render(request, 'core/listar_estados.html', data)

def detalhar_estado(request, estado_id):
    estado = get_object_or_404(Estados, pk=estado_id)
    data = {
        'nome': estado.nome,
        'uf': estado.uf,
        'versao': estado.versao,
        'flag': estado.flag.url if estado.flag else None,
        'patrias': estado.patrias.id if estado.patrias else None,
        'created_at':estado.created_at,
        'updated_at': estado.updated_at
        
    }
    return JsonResponse(data)


def salvar_estado(request):
    if request.method == 'POST':
        estado_id = request.POST.get('estado_id')
        if estado_id:  # Edição de autor existente
            estado = get_object_or_404(Estados, pk=estado_id)
            form = EstadoForm(request.POST, request.FILES, instance=estado)
        else:  # Novo estado
            form = EstadoForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('core_listar_estados')  # Redireciona após salvar
    else:
        form = EstadoForm()
    print("Tentando renderizar: estado_form.html")

    return render(request, 'estado_form.html', {'form': form})


def estado_delete_confirm(request, estado_pk):
    estado = Estados.objects.get(pk=estado_pk)
    estado.delete()
    return redirect('core_listar_estados')	

# Pátrias

def listar_patrias(request):
    data = {}
    search = request.GET.get('search')
    if search:
        data['db'] = Patrias.objects.filter(nome__icontains=search)
    else:
        data['db'] = Patrias.objects.all()	

    
    # Configura o paginador: 10 itens por página
    paginator = Paginator(data['db'], 20)  # Mostra 10 estados por página

    # Obtém o número da página da URL
    pages = request.GET.get('page')

    data['db'] = paginator.get_page(pages)
    
    
    form = PatriaForm()
    data['form'] = form
    return render(request, 'core/listar_patrias.html', data)

def salvar_patria(request):
    if request.method == 'POST':
        patria_id = request.POST.get('patria_id')
        if patria_id:  # Edição de patria existente
            patria = get_object_or_404(Patrias, pk=patria_id)
            form = PatriaForm(request.POST, request.FILES, instance=patria)
        else:  # Novo estado
            form = PatriaForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect('core_listar_patrias')  # Redireciona após salvar
    else:
        form = PatriaForm()
        print("Tentando renderizar: patria_form.html")
    return render(request, 'patria_form.html', {'form': form})

def detalhar_patria(request, patria_id):
    patria = get_object_or_404(Patrias, pk=patria_id)
    data = {
        'nome': patria.nome,
        'capital': patria.capital,
        'populacao': patria.populacao,
        'versao': patria.versao,
        'created_at': patria.created_at,
        'updated_at': patria.updated_at,
        'flag': patria.flag.url if patria.flag else None,
        'continentes': patria.continentes.id if patria.continentes else None,
    }
    return JsonResponse(data)

def patria_delete_confirm(request, patria_pk):
    patria = Patrias.objects.get(pk=patria_pk)
    patria.delete()
    return redirect('core_listar_patrias')	

