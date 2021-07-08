import requests
import json
import time
import mysql.connector
from os import system
import sys
import configparser
from Banco import Banco

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")



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

conn = mysql.connector.connect(pool_name = "mypool2", pool_size = 2,**dbconfig)
cursor = conn.cursor();


def requisitarGithub(url):
	print("Requisitando...")
	response = requests.get(url, headers=headers)
	print(response.status_code)
	return json.loads(response.text), response.status_code

def trataData(data):
	if(data):
		return data.replace("T", " ").replace("Z", "")
	else:
		return data

def requisitarPR(url, urlOriginal, idRegistro):
	result, status_code = requisitarGithub(url)

	if(status_code == 200):
			return (
				trataData(result['merged_at']),
				result['state'],
				result['number'],
				trataData(result['created_at']),
				trataData(result['updated_at']),
				trataData(result['closed_at']),
				result['additions'],
				result['deletions'],
				idRegistro
				)
	else:
		cursor.execute("""UPDATE analisegithub4.users_testam set error = 1 where urlPR = %s""",(urlOriginal,))
		conn.commit();
	

def buscarDadosPR(urlPR, id):

	urlApi = urlPR.replace("https://github.com", "https://api.github.com/repos")
	urlApi = urlApi.replace("pull", "pulls")
	return requisitarPR(urlApi, urlPR, id)

banco = Banco();

def salvarTodos(batch):



	cursor.executemany("""UPDATE analisegithub4.users_testam 
			set merged_at =  %s,
			state = %s,
			number = %s,
			created_at = %s,
			updated_at = %s,
			closed_at = %s,
			additions = %s,
			deletions = %s

			where id = %s

			""",batch)
	conn.commit();

while(True):
	if(banco.getStatusRequestV2(token) == 1):
		cursor.execute(""" SELECT urlPR, id from analisegithub4.users_testam where number is null and id >= %s and id <= %s and error is null order by id  limit 10 """, (rangeInicial, rangeFinal))
		itens = cursor.fetchall();

		arrayDados = []
		for prs in itens:
			dados = buscarDadosPR(prs[0], prs[1] )
			arrayDados.append(dados)

		salvarTodos(arrayDados)

		print("acabei")
	else:
		print("esperando proxima janela")
		time.sleep(tempoEspera)

	
