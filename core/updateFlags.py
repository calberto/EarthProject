import requests
from bs4 import BeautifulSoup
import os

# url do site para raspagem
url = "https://flagpedia.net./index"

# Enviar a requsição para o site
response = requests.get(url)
if response.status_code != 200:
    print(f"[ERRO] Não foi possível acessar a URL; {url}")
    exit()

# analisar o HTML da página com o BeautifulSoup
soup = BeautifulSoup(response.content, "html.parser")
# print(soup) 

# Encontrar todas as tags 'img' com 'src' contendo '.png'
images = soup.find_all("img", src=lambda src: src and src.endswith(".png"))
print(images)

# Criar uma pasta para salvar as imagens
outuput_folder = "imagens_png"
os.makedirs(outuput_folder, exist_ok=True)

# Fazer o download das imagens
for img in images:
    img_url = img["src"]
    if not img_url.startswith("http"):
        # Adiciona o domínio base se o link for relativo
        img_url = f"https://flagpedia.net{img_url}"
      
    # Nome do arquivo para salvar
    img_name = img_url.split("/")[-1]
    
    # Baixar as imagens
    img_data = requests.get(img_url).content
    with open(os.path.join(outuput_folder, img_name), "wb") as img_file:
        img_file.write(img_data)
        print(f"[INFO] Imagem salva: {img_name}")
print(f"[INFO] Download concluido: Imagens salvas na pasta '{outuput_folder}'")         

