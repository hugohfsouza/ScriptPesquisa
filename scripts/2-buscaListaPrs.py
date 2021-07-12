import requests
import json
import time
import mysql.connector
from Banco import Banco
import configparser

import sys


if(len(sys.argv) <= 3):
	print("Está faltando parametros")
	exit();

	
config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

tempoEspera 	= int(config.get("GERAL", "tempoEsperaProximaValidacaoToken"))
banco 			= Banco();

token 	= config.get("TOKENS", sys.argv[1])
headers	= {'Authorization': token}

rangeInicial 	= sys.argv[2]
rangeFinal 		= sys.argv[3]



def requisitarGithub(url, headerExtra=None):
    url = "https://api.github.com/"+str(url)
    response = requests.get(url, headers=headers)
    return json.loads(response.text)

def buscarPrs(repo):
	pagina = 1

	result = requisitarGithub("repos/"+str(repo[1])+"/pulls?state=all&sort=created&direction=desc&per_page=100&page="+str(pagina))
	while(len(result) > 0):
		for pr in result:
			try:
				banco.salvarPR(
					repo[0], 
					pr['number'], 
					pr['state'], 
					pr['url'],
					pr['user']['login'], 
					pr['created_at'], 
					pr['updated_at'],
					pr['closed_at'],
					pr['merged_at']
				)
			except Exception as e:
				pass
				
		pagina += 1
		result = requisitarGithub("repos/"+str(repo[1])+"/pulls?state=all&sort=created&direction=desc&per_page=100&page="+str(pagina))
		print("["+str(repo[1])+"] pagina: "+str(pagina))

	banco.registrarPRsEncontrados(repo[0])
	pass


while(True):
	if(banco.getStatusRequestV2(token) == 1):
		repo = banco.getRepoParaRecuperarPRsRange(rangeInicial, rangeFinal)
		if(repo):
			buscarPrs(repo)
			print(repo[1]+" concluido")
		else:
			print("conclui tudo")
			time.sleep(tempoEspera)

		
	else:
		print("esperando proxima janela")
		time.sleep(tempoEspera)

	
	