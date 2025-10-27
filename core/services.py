import os
import django

# Configura Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'terra.settings')
django.setup()

from core.models import Patrias
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

def fetch_population_data():
    print("Iniciando o processo de scraping...")
    url = "https://www.worldometers.info/world-population/population-by-country/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table")

    if table is None:
        print("Erro: A tabela não foi encontrada.")
        return None

    html_table = str(table)
    df = pd.read_html(StringIO(html_table))[0]

    df = df.rename(columns={"Country (or dependency)": "nome", "Population  (2024)": "populacao"})
    df['populacao'] = df['populacao'].str.replace(",", "").astype(int)

    return df[['nome', 'populacao']]

def update_population_from_dataframe(df):
    for _, row in df.iterrows():
        try:
            patria = Patrias.objects.get(nome=row['nome'])
            patria.populacao = row['populacao']
            patria.save()
        except Patrias.DoesNotExist:
            print(f"Pátria não encontrada: {row['nome']}")
