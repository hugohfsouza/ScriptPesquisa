import requests
import json
import time
import mysql.connector
from Banco import Banco
import configparser


config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

tempoEspera 	= int(config.get("GERAL", "tempoEsperaProximaValidacaoToken"))
token    		= config.get("TOKENS", "token1")
banco 			= Banco();
headers 		= {'Authorization': token}


def requisitarGithub(url, headerExtra=None):
    url = "https://api.github.com/"+str(url)
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def buscarPrs(repo):
	pagina = 1

	result = requisitarGithub("repos/"+str(repo[2])+"/pulls?state=all&sort=created&direction=desc&per_page=100&page="+str(pagina))
	while(len(result) > 0):
		for pr in result:
			try:
				banco.salvarPR(
					repo[0], 
					pr['id'], 
					pr['number'], 
					pr['state'], 
					pr['locked'], 
					pr['user']['login'], 
					pr['user']['id'], 
					pr['url'], 
					pr['created_at'], 
					pr['updated_at']
				)
			except Exception as e:
				pass
		
		pagina += 1
		result = requisitarGithub("repos/"+str(repo[2])+"/pulls?state=all&sort=created&direction=desc&per_page=100&page="+str(pagina))
		print("["+str(repo[2])+"] pagina: "+str(pagina))

	banco.registrarPRsEncontrados(repo[0])
	pass


while(True):

	if(banco.getStatusRequestV2(token) == 1):
		repo = banco.getRepoParaRecuperarPRs()
		buscarPrs(repo)
		print(repo[2]+" concluido")
		
	else:
		print("esperando proxima janela")
		time.sleep(tempoEspera)

	
	