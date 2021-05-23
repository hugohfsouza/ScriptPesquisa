import requests
import json
import time
from Banco import Banco
import configparser
from os import system
import sys
import re

system("title Recupera Nomes dos Usuários")

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


if(len(sys.argv) <= 3):
	print("Está faltando parametros")
	exit();

banco 	= Banco();
token 	= config.get("TOKENS", sys.argv[1])
headers	= {'Authorization': token}

rangeInicial 	= sys.argv[2]
rangeFinal 		= sys.argv[3]
tempoEspera 	= int(config.get("GERAL", "tempoEsperaProximaValidacaoToken"))

# banco.importUserPRtoUser()


def requisitarGithub(nameUser, headerExtra=None):
    url = "https://api.github.com/users/"+str(nameUser)
    response = requests.get(url, headers=headers)
    return response.status_code, json.loads(response.text)


def recuperarDados(user):
	print(user)
	statusCode, response = requisitarGithub(user)
	if(statusCode == 200):
	
		idGithub			= response['id']
		typeUser			= response['type']
		company 			= response['company']
		blog 				= response['blog']
		location 			= response['location']
		email 				= response['email']
		twitter_username 	= response['twitter_username']
		public_repos 		= response['public_repos']
		public_gists 		= response['public_gists']
		followers 			= response['followers']
		following 			= response['following']
		login 				= user
		name 				= response['name']

		banco.saveUser(idGithub, typeUser, company, blog, location, email, twitter_username, public_repos, public_gists, followers, following, login, name)
	else:
		banco.saveUserErro(user)


while(True):
	if(banco.getStatusRequestV2(token) == 1):
		user = banco.getUserToAnalyser(rangeInicial, rangeFinal)

		if(user):
			recuperarDados(user[0]);

		else:
			print("Todo Range foi analizado")
			time.sleep(5)
	else:
		print("esperando proxima janela")
		time.sleep(tempoEspera)
	

