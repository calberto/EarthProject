
import requests
from bs4 import BeautifulSoup

link = "https://www.englishforbrazilianpeople.com/2014/07/paises-capitais-em-ingles-moedas-idiomas.html"

requisicao = requests.get(link)
print(requisicao)
# print(requisicao.text)
site = BeautifulSoup(requisicao.text, "html.parser")
# print(site.prettify())
titulo = site.find('title')
print('titulo é:', titulo)
pesquisa = site.find_all("table")
print(pesquisa[0])
