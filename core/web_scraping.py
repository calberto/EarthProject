import requests
from bs4 import BeautifulSoup
import pandas as pd
from io import StringIO

def fetch_population_data():
    url = "https://www.worldometers.info/world-population/population-by-country/"
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida
    if response.status_code != 200:
        raise Exception(f"Erro ao acessar {url}: Status code {response.status_code}")
    
    # Analisa o conteúdo HTML da página
    
    soup = BeautifulSoup(response.content, "html.parser")
    # Tente localizar a tabela correta
    table = soup.find("table")
    
    if table is None:
        print("Tabela não encontrada.")
    else:
        print("Tabela encontrada!")
        table_html = str(table)
        df = pd.read_html(StringIO(table))[0]
        print(df.head())  # Verifique o conteúdo
    
    # Renomeia colunas para facilitar a manipulação
    df = df.rename(columns={
        "Country (or dependency)": "nome",
        "Population  (2024)": "populacao",
        "Yearly Change": "mudanca_anual",
        "Net Change": "mudanca_liquida",
        "Density (P/Km²)": "densidade",
        "Land Area (Km²)": "area_terrestre",
        "Migrants (net)": "migrantes",
        "Fert. Rate": "taxa_fertilidade",
        "Med. Age": "idade_media",
        "Urban Pop %": "pop_urbana",
        "World Share": "participacao_mundial"
    })
    
    # Verifica se os valores são strings e aplica tratamento
    if df['populacao'].dtype == 'object':  # Se os valores forem strings
        df['populacao'] = df['populacao'].str.replace(",", "").astype(int)
    else:  # Se os valores já forem numéricos
        df['populacao'] = df['populacao'].fillna(0).astype(int)
    
    print(df)
    return df[['nome', 'populacao']]  # Retorna apenas as colunas relevantes
    
