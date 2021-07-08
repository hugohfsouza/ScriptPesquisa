import requests
import json
import time
import mysql.connector
from Banco import Banco
from os import system
import sys
import configparser
import random

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





dbconfig = {
    "host":     config.get("MYSQL", "host"),
    "user":     config.get("MYSQL", "user"),
    "passwd":   config.get("MYSQL", "passwd"),
    "db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool1", pool_size = 1,**dbconfig)
cursor = conn.cursor();


banco = Banco();

def requisitarGithub(url, headerExtra=None):
	while(True):
		print("Requisitando...")
		response = requests.get(url, headers=headers)
		print(response.status_code)
		if(response.status_code == 200 or response.status_code == 404):
			break
		else:
			time.sleep(5)
	
	
	return json.loads(response.text), response.status_code




def buscarArquivos(pullRequest, urlOriginal, idRegistro):
	pagina = 1
	result, status_code = requisitarGithub(str(pullRequest)+"/files?per_page=100&page="+str(pagina))

	while(len(result) > 0 and (not 'errors' in result) and status_code == 200 ):
		listaArquivosPR = []
		print(pullRequest)
		for file in result:
			listaArquivosPR.append(
				(
					urlOriginal, 
					file['filename'],
					file['additions'],
					file['deletions'],
					file['sha']
				)
			)

		try:
			
			for registro in listaArquivosPR:
				try:
					cursor.execute("""INSERT INTO  analisegithub4.pull_request_files(urlPR, filename, additions, deletions, sha) values (%s,%s,%s,%s,%s)
				""",(registro[0], registro[1], registro[2], registro[3], registro[4]))
					conn.commit();
				except Exception as e:
					pass
				
				

		except Exception as e:
			print(e)
			pass
	
		if(len(result) == 100):
			pagina += 1
			result, status_code = requisitarGithub(str(pullRequest)+"/files?per_page=100&page="+str(pagina))
		else:
			result = []

	
	cursor.execute("""update analisegithub4.users_testam set arquivos_encontrados = 1 where id = %s """,(idRegistro,))
	conn.commit();

	pass


def intermediadio(urlOriginal, id):
	urlApi = urlOriginal.replace("https://github.com", "https://api.github.com/repos")
	urlApi = urlApi.replace("pull", "pulls")

	buscarArquivos(urlApi, urlOriginal, id)



while(True):
	if(banco.getStatusRequestV2(token) == 1):
		cursor.execute(""" SELECT urlPR, id from analisegithub4.users_testam where arquivos_encontrados is null and id >= %s and id <= %s limit 100 """, (rangeInicial, rangeFinal))
		itens = cursor.fetchall();

		for link in itens:
			intermediadio(link[0], link[1])

		print("acabei")

