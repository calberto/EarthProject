if __name__ == "__main__":
    import requests
    import pandas as pd
    from bs4 import BeautifulSoup
    from io import StringIO
    from core.models import Patrias  # Certifique-se que funciona no seu ambiente Django

    def fetch_population_data():
        print("[INFO] Iniciando o processo de scraping...")  # Depuração inicial
        url = "https://www.worldometers.info/world-population/population-by-country/"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find("table")
        
        if table is None:
            print("[ERRO] A tabela não foi encontrada na página.")
            return None  # Sai da função se a tabela não for encontrada
        
        print("[INFO] Tabela encontrada!")  # Mensagem de confirmação
        
        # Lê a tabela em um DataFrame
        html_table = str(table)
        df = pd.read_html(StringIO(html_table))[0]
        
        print("[INFO] DataFrame lido com sucesso!")  # Verifica se o DataFrame foi lido
        print("[INFO] Colunas disponíveis no DataFrame:", df.columns)

        # Renomeia colunas para facilitar a manipulação
        try:
            df = df.rename(columns={"Country (or dependency)": "nome", "Population  (2024)": "populacao"})
        except KeyError as e:
            print("[ERRO] Falha ao renomear colunas. Certifique-se de que o nome das colunas está correto:", e)
            return None
        
        # Remove vírgulas e formata a coluna de população
        try:
            df['populacao'] = df['populacao'].str.replace(",", "").astype(int)
        except Exception as e:
            print("[ERRO] Problema ao formatar a coluna de população:", e)
            return None
        
        print("[INFO] Primeiras linhas do DataFrame após renomeação e formatação:")
        print(df.head())
        
        return df[['nome', 'populacao']]  # Retorna apenas as colunas relevantes

    def update_population_from_dataframe(df):
        print("[INFO] Iniciando a atualização da tabela 'Patrias' no banco de dados...")
        atualizacoes = 0
        for _, row in df.iterrows():
            try:
                # Busca a pátria pelo nome
                patria = Patrias.objects.get(nome=row['nome'])
                
                # Atualiza o campo população
                patria.populacao = row['populacao']
                patria.save()
                atualizacoes += 1
                print(f"[INFO] População atualizada: {patria.nome} -> {patria.populacao}")
            except Patrias.DoesNotExist:
                print(f"[AVISO] Pátria não encontrada: {row['nome']}")
        
        print(f"[INFO] Total de atualizações realizadas: {atualizacoes}")

    # Bloco principal
    df = fetch_population_data()  # Chama a função para buscar os dados
    if df is not None and not df.empty:  # Verifica se o DataFrame foi retornado corretamente
        print("[INFO] Dados de população obtidos com sucesso. Atualizando o banco de dados...")
        update_population_from_dataframe(df)
    else:
        print("[ERRO] O DataFrame está vazio ou não foi gerado corretamente. O banco de dados não será atualizado.")
