import sys
import os
import django
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import StringIO

# Configurar o caminho do projeto e o Django
sys.path.append("/home/carlos/Desenvolvimento/Python/Workspace/earthProject")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terra.settings')
django.setup()

from core.models import Patrias  # Certifique-se de que o nome do app está correto

def fetch_population_data():
    print("[INFO] Iniciando o processo de scraping...")
    url = "https://www.worldometers.info/world-population/population-by-country/"
    response = requests.get(url)

    if response.status_code != 200:
        print(f"[ERRO] Falha na requisição. Código de status: {response.status_code}")
        return None

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")

    if table is None:
        print("[ERRO] A tabela não foi encontrada no HTML.")
        return None

    print("[INFO] Tabela encontrada! Extraindo os dados...")
    html_table = str(table)

    try:
        df = pd.read_html(StringIO(html_table))[0]
    except ValueError as e:
        print(f"[ERRO] Falha ao criar o DataFrame: {e}")
        return None

    if df.empty:
        print("[ERRO] O DataFrame criado está vazio.")
        return None

    print("[INFO] DataFrame lido com sucesso!")
    print(df.head())  # Mostra os primeiros registros para verificar

    # Renomeia as colunas relevantes e trata os dados
    df = df.rename(columns={"Country (or dependency)": "nome", "Population  (2024)": "populacao"})
    try:
        df['populacao'] = df['populacao'].astype(str).str.replace(",", "").astype(int)
    except Exception as e:
        print(f"[ERRO] Problema ao formatar a coluna de população: {e}")
        return None

    return df[['nome', 'populacao']]  # Retorna apenas as colunas necessárias

def update_population_from_dataframe(df):
    if df is None or df.empty:
        print("[ERRO] O DataFrame fornecido está vazio ou é inválido.")
        return {"atualizados": 0, "novos": 0}

    print("[INFO] Iniciando a atualização da tabela 'Patrias' no banco de dados...")
    atualizacoes = 0
    novos = 0
    for _, row in df.iterrows():
        try:
            patria = Patrias.objects.get(nome=row['nome'])
            patria.populacao = row['populacao']
            patria.save()
            atualizacoes += 1
            print(f"[INFO] População atualizada: {patria.nome} -> {patria.populacao}")
        except Patrias.DoesNotExist:
            Patrias.objects.create(nome=row['nome'], populacao=row['populacao'])
            novos += 1
            print(f"[INFO] Nova pátria criada: {row['nome']} -> {row['populacao']}")

    print(f"[INFO] Total de atualizações realizadas: {atualizacoes}")
    print(f"[INFO] Total de novos registros criados: {novos}")

    return {"atualizados": atualizacoes, "novos": novos}
