import requests
import json
import time
from Banco import Banco
import configparser
from os import system
import sys

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


if(len(sys.argv) <= 3):
	print("Está faltando parametros")
	exit();


tempoEspera 	= int(config.get("GERAL", "tempoEsperaProximaValidacaoToken"))
token 			= config.get("TOKENS", sys.argv[1])
banco 			= Banco();
headers 		= {'Authorization': token}

rangeInicial 	= sys.argv[2]
rangeFinal 		= sys.argv[3]



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
				banco.atualizaPr(pr['id'], pr['closed_at'], pr['merged_at'])
			except Exception as e:
				pass
		
		pagina += 1
		result = requisitarGithub("repos/"+str(repo[2])+"/pulls?state=all&sort=created&direction=desc&per_page=100&page="+str(pagina))
		print("["+str(repo[2])+"] pagina: "+str(pagina))

	banco.registrarPRsAnalisados(repo[0])
	pass


while(True):

	if(banco.getStatusRequestV2(token) == 1):
		repo = banco.getRepoParaRecuperarPRsParallel(rangeInicial, rangeFinal)
		if(repo):
			buscarPrs(repo)
			print(repo[2]+" concluido")
		else:
			print("Terminei meu range")
			time.sleep(tempoEspera)
	else:
		print("esperando proxima janela")
		time.sleep(tempoEspera)
