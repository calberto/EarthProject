from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Continente, Patrias, Estados, Cidades
from .forms import ContinenteForm, PatriaForm, EstadoForm, CidadeForm
from django.contrib.auth.decorators import login_required


# def home(request):
    # context = {'mensagem':'Olá Ninho' }
    # return render(request, 'core/index.html', context)

# @login_required
def listar_continentes(request):
    continentes = Continente.objects.all()
    return render(request, 'core/listar_continentes.html', {'continentes': continentes})

def detalhar_continente(request, id):
	continente = get_object_or_404(Continente, id=id)
	return render(request, 'core/detalhar_continente.html', {'continente': continente})	

def adicionar_continente(request):
    if request.method == 'POST':
        form = ContinenteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_continentes')
        else:
            return render(request, 'core/adicionar_continente.html', {'form': form})
    else:
        form = ContinenteForm()
        return render(request, 'core/adicionar_continente.html', {'form': form})

# @login_required
def listar_patrias(request):
    patrias = Patrias.objects.all()
    return render(request, 'core/listar_patrias.html', {'patrias': patrias})

def detalhar_patria(request, id):
	patria = get_object_or_404(Patrias, id=id)
	return render(request, 'core/detalhar_patria.html', {'patria': patria})	

def adicionar_patria(request):
    if request.method == 'POST':
        form = PatriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_patrias')
        else:
            return render(request, 'core/adicionar_patria.html', {'form': form})
    else:
        form = PatriaForm()
        return render(request, 'core/adicionar_patria.html', {'form': form})



# @login_required
def listar_estados(request):
    estados = Estados.objects.all()
    return render(request, 'core/listar_estados.html', {'estados': estados})

def detalhar_estado(request, id):
	estado = get_object_or_404(Estados, id=id)
	return render(request, 'core/detalhar_estado.html', {'esstado': estado})	

def adicionar_estado(request):
    if request.method == 'POST':
        form = EstadoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_estados')
        else:
            return render(request, 'core/adicionar_estado.html', {'form': form})
    else:
        form = EstadoForm()
        return render(request, 'core/adicionar_estado.html', {'form': form})

# @login_required
def listar_cidades(request):
    cidades = Cidades.objects.all()
    return render(request, 'core/listar_cidades.html', {'cidades': cidades})

def detalhar_cidade(request, id):
	cidade = get_object_or_404(Cidades, id=id)
	return render(request, 'core/detalhar_pcidade.html', {'cidade': cidade})	

def adicionar_cidade(request):
    if request.method == 'POST':
        form = CidadeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_cidades')
        else:
            return render(request, 'core/adicionar_cidade.html', {'form': form})
    else:
        form = CidadeForm()
        return render(request, 'core/adicionar_cidade.html', {'form': form})
