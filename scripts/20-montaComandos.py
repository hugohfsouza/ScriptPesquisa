import requests
import json
import mysql.connector
import os
import sys
import configparser
import threading

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


dbconfig = {
    "host":     config.get("MYSQL", "host"),
    "user":     config.get("MYSQL", "user"),
    "passwd":   config.get("MYSQL", "passwd"),
    "db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(pool_name = "mypool2", pool_size = 2,**dbconfig)
cursor = conn.cursor();




# sqlDados = """ SELECT id FROM analisegithub4.users_testam WHERE number IS NULL  """
# comando = "python .\\15-recuperaDadosPRUser.py #token# #inicio# #fim#"

# sqlDados = """ SELECT id FROM analisegithub4.users_testam WHERE arquivos_encontrados IS NULL  """
# comando = "python .\\16-RecuperaArquivosPRUser.py #token# #inicio# #fim#"

sqlDados = """SELECT id, url  from analisegithub5.pull_requests where hasTest is null and analisado = 0 """
comando = "python .\\4-recuperaArquivosPR.py #token# #inicio# #fim#"


quantidadeJanelas = 2

cursor.execute(sqlDados)
lista = cursor.fetchall();

quantidadePorComando = int(len(lista)/quantidadeJanelas)



idInicial = 0
idFinal = 0

numeroToken = 1

def abrirCmd(comando):
	os.system("start /wait cmd /k "+comando)

for i in range(quantidadeJanelas):
	if(numeroToken > 12):
		numeroToken = 1

	token = numeroToken;
	numeroToken += 1
	


	cursor.execute(sqlDados+" and id > %s limit "+str(quantidadePorComando), (idInicial,))
	listaIds = cursor.fetchall();

	for x in listaIds:
		idFinal = x[0]

	comandoAtual = comando.replace("#token#", "token"+str(token))
	comandoAtual = comandoAtual.replace("#inicio#", str(idInicial))
	comandoAtual = comandoAtual.replace("#fim#", str(idFinal))

	idInicial = idFinal
	print(comandoAtual)
	x = threading.Thread(target=abrirCmd, args=(comandoAtual,))
	x.start()


	