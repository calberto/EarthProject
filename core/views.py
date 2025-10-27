from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Continentes, Patrias, Estados, Cidades
from django.db.models import Q
from .forms import ContinenteForm, PatriaForm, EstadoForm, CidadeForm, NewContinenteForm
from django.contrib.auth.decorators import login_required
import imghdr
import subprocess
from django.http import HttpResponse
from django.core.paginator import Paginator
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from core.atualiza import fetch_population_data, update_population_from_dataframe
from django.http import JsonResponse
import traceback

import sys
import os
import django
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO
from django.http import JsonResponse, HttpResponseNotAllowed
from django.template.loader import render_to_string
from .models import Continentes
from .forms import ContinenteForm
from django.contrib import messages
from django.utils import timezone



def home(request):
    context = {'mensagem' : 'Olá Ninho!'}
    return render(request, 'core/index.html', context)

def home_continente(request):
    # Exemnplo de view para a página inicial
    	return render(request, 'core/home_continente.html')

# @login_required

def listar_continentes(request):
    data = {}

    # Busca por nome ou sigla
    search = request.GET.get('search')
    order = request.GET.get('order_by', 'nome')  # Campo para ordenar
    direction = request.GET.get('direction', 'asc')  # Direção (asc ou desc)

    if search:
                data['db'] = Continentes.objects.filter(
                    Q(nome__icontains=search) 
                )

    else:
        data['db'] = Continentes.objects.all()

    # Ordenação
    if direction == 'desc':
        order = f'-{order}'

    data['db'] = data['db']
    # Configura o paginador: 10 itens por página
    paginator = Paginator(data['db'], 8)  # Mostra 10 estados por página

    # Obtém o número da página da URL
    pages = request.GET.get('page')

    data['db'] = paginator.get_page(pages)


    form = ContinenteForm()
    data['form'] = form
    return render(request, 'core/listar_continentes.html', data)



def salvar_continente(request):
    if request.method == 'POST':
        # Verifica se há um ID no formulário para determinar se é atualização
        continente_id = request.POST.get('continente_id')
        if continente_id:
            # Atualização: Busca o continente existente
            continente = get_object_or_404(Continentes, pk=continente_id)
            form = ContinenteForm(request.POST, request.FILES, instance=continente)
        else:  # Novo autor
            form = ContinenteForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Continente salvo com sucesso!')
            return redirect('core_listar_continentes')  # Redireciona para a lista
        else:
            
            messages.error(request, 'Erro ao salvar o continente. Verifique os dados.')
    else:
        form = ContinenteForm()

    return render(request, 'continente_form.html', {'form': form})
    


def detalhar_continente(request, continente_id):
    print(f"Ninho entrou na detalhar_continente...")
    print("View detalhar_continente chamada com ID:", continente_id)
    continente = get_object_or_404(Continentes, pk=continente_id)
    print("Objeto encontrado:", continente)
    print("DEBUG - Continente carregado:", continente)
    print("DEBUG - Nome:", continente.nome)
    print("DEBUG - Versão:", continente.versao)
    
    data = {
        'nome': continente.nome,
        'versao': continente.versao,
        'created_at': continente.created_at,
        'updated_at': continente.updated_at
    }
    return JsonResponse(data)

def continente_delete_confirm(request, continente_pk):
    continente = Continentes.objects.get(pk=continente_pk)
    continente.delete()
    return redirect('core_listar_continentes')

def novo_continente(request):
    form = ContinenteForm()
    return render(request, 'core/partials/continente_form.html', {'form': form})

# Cidades
def listar_cidades(request):
    data = {}

    # Busca por nome ou sigla
    search = request.GET.get('search')
    order = request.GET.get('order_by', 'nome')  # Campo para ordenar
    direction = request.GET.get('direction', 'asc')  # Direção (asc ou desc)

    if search:
                data['db'] = Cidades.objects.filter(
                    Q(nome__icontains=search) | Q(estados__nome__icontains=search)
                )

    else:
        data['db'] =  Cidades.objects.select_related('estados').all().order_by('nome')


    # Ordenação
    if direction == 'desc':
        order = f'-{order}'

    data['db'] = data['db']

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

    # Busca por nome ou sigla
    search = request.GET.get('search')
    order = request.GET.get('order_by', 'nome')  # Campo para ordenar
    direction = request.GET.get('direction', 'asc')  # Direção (asc ou desc)

    if search:
        data['db'] = Estados.objects.filter(nome__icontains=search) | Estados.objects.filter(uf__icontains=search)

    else:
        data['db'] = Estados.objects.all()

    # Ordenação
    if direction == 'desc':
        order = f'-{order}'

    data['db'] = data['db']

    # Configura o paginador: 10 itens por página
    paginator = Paginator(data['db'], 15)  # Mostra 10 estados por página

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
    print(f"Método: {request.method}")
    print(f"POST data: {request.POST}")
    
    if request.method == 'POST':
        estado_id = request.POST.get('estado_id')
        print(f"Estado ID: {estado_id}")
        
        if estado_id:
            # Atualização
            estado = get_object_or_404(Estados, pk=estado_id)
            form = EstadoForm(request.POST, request.FILES, instance=estado)
            print("Modo: Atualização")
        else:
            # Novo estado
            form = EstadoForm(request.POST, request.FILES)
            print("Modo: Novo registro")
        
        print(f"Form é válido? {form.is_valid()}")
        if form.is_valid():
            estado_salvo = form.save()
            print(f"Estado salvo: {estado_salvo}")
            messages.success(request, 'Estado salvo com sucesso!')
            return redirect('core_listar_estados')
        else:
            print(f"Erros do form: {form.errors}")
            messages.error(request, 'Erro ao salvar o estado. Verifique os dados.')
    else:
        form = EstadoForm()
    
    return render(request, 'core/estado_form.html', {'form': form})



def estado_delete_confirm(request, estado_pk):
    estado = Estados.objects.get(pk=estado_pk)
    estado.delete()
    return redirect('core_listar_estados')

# Pátrias

def listar_patrias(request):
    data = {}

    # Busca por nome ou sigla
    search = request.GET.get('search')
    order = request.GET.get('order_by', 'nome')  # Campo para ordenar
    direction = request.GET.get('direction', 'asc')  # Direção (asc ou desc)

    if search:
        data['db'] = Patrias.objects.filter(nome__icontains=search) | Patrias.objects.filter(capital__icontains=search) | Patrias.objects.filter(populacao__icontains=search)
        

    else:
        data['db'] = Patrias.objects.all()

    # Ordenação
    if direction == 'desc':
        order = f'-{order}'

    data['db'] = data['db']

    # Configura o paginador: 10 itens por página
    paginator = Paginator(data['db'], 15)  # Mostra 10 patrias por página

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

def atualizar_dados(request):
    df = fetch_population_data()  # Obtém os dados do scraping
    if df is not None and not df.empty:
        update_population_from_dataframe(df)  # Atualiza o banco de dados
        return JsonResponse({
            "mensagem": "Dados atualizados com sucesso!"
        })
    else:
        return JsonResponse({
            "mensagem": "Erro: o DataFrame está vazio ou inválido."
        }, status=400)

def executar_script(request):

    try:
        # Caminho para o ambiente virtual
        python_executable = "/home/carlos/Desenvolvimento/Python/Workspace/earthProject/envEarth/bin/python"

        # Executa o script Python
        import subprocess

        resultado = subprocess.run(
            ["/home/carlos/Desenvolvimento/Python/Workspace/earthProject/envEarth/bin/python",
            "/home/carlos/Desenvolvimento/Python/Workspace/earthProject/core/atualiza.py"],
            capture_output=True, text=True
        )

        # Exibindo a saída e o erro (se houver)
        print("Saída:")
        print(resultado.stdout)

        print("Erro:")
        print(resultado.stderr)

        # Retorna o resultado do script
        return JsonResponse({
            "mensagem": "Script executado com sucesso!",
            "saida": resultado.stdout,
            "erro": resultado.stderr
        })
    except Exception as e:
        erro = traceback.format_exc()
        print(f"[ERRO] Falha ao executar o script: {erro}")
        return JsonResponse({"status": "erro", "mensagem": str(e), "detalhes": erro})
"""
def atualizar_patrias(request):
    df = fetch_population_data()
    if df is None or df.empty:
        return JsonResponse({
            "mensagem": "Erro ao buscar os dados.",
            "erro": "O DataFrame está vazio ou não foi gerado corretamente."
        }, status=400)

    update_population_from_dataframe(df)
    return JsonResponse({"mensagem": "Banco de dados atualizado com sucesso!"})

def listar_patrias(request):
    patrias = Patrias.objects.all().values('nome', 'populacao')
    return JsonResponse(list(patrias), safe=False)

def update_population(request):
    if request.method == "POST":
        try:
            # Obtém o DataFrame de dados de população
            df = fetch_population_data()

            # Passa o DataFrame para a função de atualização
            update_population_from_dataframe(df)

            # Redireciona para a página principal após sucesso
            return redirect('listar_patrias')
        except Exception as e:
            # Retorna uma resposta com o erro
            return HttpResponse(f"Ocorreu um erro: {e}", status=500)
    return HttpResponse("Método não permitido", status=405)

from .models import Patrias

def update_population_from_dataframe(df):
    for _, row in df.iterrows():
        try:
            # Busca a pátria pelo nome
            patria = Patrias.objects.get(nome=row['nome'])
            # Atualiza o campo população
            patria.populacao = row['populacao']
            patria.save()
        except Patrias.DoesNotExist:
            print(f"Pátria não encontrada: {row['nome']}")


def export_to_csv(queryset, filename="patrias.csv"):
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'População', 'Capital', 'Continente'])

    for patria in queryset:
        writer.writerow([patria.nome, patria.populacao, patria.capital, patria.continentes.nome])

    return response

def export_to_pdf(queryset, filename="patrias.pdf"):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.drawString(100, 800, "Relatório de Populações")
    y = 750

    for patria in queryset:
        pdf.drawString(50, y, f"{patria.nome} - {patria.populacao}")
        y -= 20

    pdf.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()

    return response
"""
