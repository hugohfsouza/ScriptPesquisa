import requests
import json
import time
import mysql.connector
from Banco import Banco
from os import system
import sys
import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")
tempoEspera 	= int(config.get("GERAL", "tempoEsperaProximaValidacaoToken"))

if(len(sys.argv) <= 3):
	print("Está faltando parametros")
	exit();


token 	= config.get("TOKENS", sys.argv[1])
headers	= {'Authorization': token}

rangeInicial 	= sys.argv[2]
rangeFinal 		= sys.argv[3]



system("title Pega Arquivos range "+str(rangeInicial)+" - "+str(rangeFinal)+" "+str(token))

banco = Banco();

def requisitarGithub(url, headerExtra=None):
	print("Requisitando...")
	response = requests.get(url, headers=headers)
	print(response.status_code)
	return json.loads(response.text)




def buscarArquivos(pullRequest):

	pagina = 1
	result = requisitarGithub(str(pullRequest[1])+"/files?per_page=100&page="+str(pagina))
	
	while(len(result) > 0 and (not 'errors' in result) ):
		listaArquivosPR = []
		print(pullRequest[0])

		for file in result:
			listaArquivosPR.append(
				(
					pullRequest[0], 
					file['filename'],
					file['additions'],
					file['deletions'],
					file['sha']
				)
			)

		try:
			banco.salvarFilesPRBulk(listaArquivosPR)
		except Exception as e:
			print(e)
			pass
	
		if(len(result) == 100):
			pagina += 1
			result = requisitarGithub(str(pullRequest[1])+"/files?per_page=100&page="+str(pagina))
		else:
			result = []


	banco.registraArquivosEncontrados(pullRequest)
	pass



while(True):
	if(banco.getStatusRequestV2(token) == 1):
		pullRequests = banco.getPullRequestsToAnalizerRange(rangeInicial, rangeFinal)
		
		for pullRequest in pullRequests:
			print(pullRequest[0])
			if(pullRequest):
				buscarArquivos(pullRequest)
				print("id: "+ str(pullRequest[0]))
				print("---------------------------")
			else:
				print("Todos os itens do range foram analisados")
				time.sleep(tempoEspera)
	else:
		print("esperando proxima janela")
		time.sleep(tempoEspera)

