import requests
import json
import time
from Banco import Banco
from datetime import datetime
from os import system
import configparser

system("title Verifica Limites de Requests no GITHUB")

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


tokens = []
configuracao  = config.items("TOKENS")
for x in configuracao:
	tokens.append(x[1])

banco 			= Banco();
limiteMaximo 	= int(config.get("GERAL", "limiteMaximoAntesDePararOsRequests"))


def verificarUsoApiGithub():
	for token in tokens:
		headers = {'Authorization': token, 'Accept': 'application/vnd.github.v3+json'}
		url = "https://api.github.com/rate_limit"
		response = requests.get(url, headers=headers)
		y = json.loads(response.text)


		if(y["resources"]["core"]['remaining'] < limiteMaximo):
			banco.setStatusRequestV2(0, token)
		else:
			banco.setStatusRequestV2(1, token)

		dt_object = datetime.fromtimestamp(y["resources"]["core"]['reset'])
		print("[Max Reqs] "+str(y["resources"]["core"]['remaining']) + " [Reset] "+str(dt_object) + " [TOKEN] "+str(token) )


banco.verificarExistenciaDeTokensNaBase(tokens)

while(True):
	verificarUsoApiGithub()
	print("")
	time.sleep(2)