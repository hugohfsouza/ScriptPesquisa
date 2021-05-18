import requests
from bs4 import BeautifulSoup
from Banco import Banco
import time
import configparser


config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

nomeFile    = config.get("GERAL", "nomeArquivoRepoComTeste")
arquivo     = open(nomeFile, "a")

banco = Banco();

def enviarRequest(url):
    time.sleep(0.500)
    result = requests.get(url)
    if(result.status_code == 200):
        return result

    else:
        time.sleep(10)
        result = requests.get(url)
        if(result.status_code == 200):
            return result
        else:    
            return False



def verificar(url):
    result = enviarRequest(url)
    if(result == False):
        return "Error"

    soup = BeautifulSoup(result.text, "lxml")
    listaItens = soup.find_all("div", class_="code-list-item-public")
    count = 0;

    for x in listaItens:
        aux = BeautifulSoup(x.prettify(), "lxml")
        item = aux.find("a")
        
        if 'TEST' in item.text.upper():
            count += 1

    if count >= 3:
        return True
    else:
        return False

lista = banco.getListaReposParaVerificarTestes();
    
for repo in lista:
    repo = repo[0]
    url = "http://github.com/"+repo+"/search?q=test"
    print(str(repo)+"|"+str(verificar(url)))
    arquivo.write(str(repo)+"|"+str(verificar(url))+"\n")



