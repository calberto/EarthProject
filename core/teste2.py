# Introdução ao Beautifulsoup - Raspagem de Dados com Python
import requests
from bs4 import BeautifulSoup # Ótimo para sites estáticos

# Dica: quando copia o link interessado, copia o início até o primeiro &
link = "https://flagpedia.net./index/"
requisicao = requests.get(link)
# Para saber se correu tudo certo com o link-retorna status 200 logo no início do print(requisicao)
print(requisicao)
# Para mostrar todo o conteudo da página html da pesquisa retornada
# print(requisicao.text)
site = BeautifulSoup(requisicao.text, "html.parser")
# print(site.prettify())
titulo = site.find_all("table")
print(titulo)
