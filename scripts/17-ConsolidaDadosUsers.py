import mysql.connector
import json
import time
import configparser
import sys

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

rangeInicial 	= sys.argv[1]
rangeFinal 		= sys.argv[2]


class Banco():

	def __init__(self):
		dbconfig = {
			"host":     config.get("MYSQL", "host"),
		    "user":     config.get("MYSQL", "user"),
		    "passwd":   config.get("MYSQL", "passwd"),
		    "db":       config.get("MYSQL", "db"),
		}

		self.conn = mysql.connector.connect(pool_name = "mypool", pool_size = 2,**dbconfig)
		self.cursor = self.conn.cursor();

	def getCountComTeste(self, urlPR):
		retorno = 0
		linhas = self.cursor.execute("""SELECT count(1) from analisegithub4.pull_request_files where urlPR = %s and filename like '%test%'""", (urlPR,))
		for result in self.cursor.fetchall():
			retorno = result[0]

		return retorno

	def getCountSemTeste(self, urlPR):
		retorno = 0;
		linhas = self.cursor.execute("""SELECT count(1) from analisegithub4.pull_request_files where urlPR = %s and filename not like '%test%'""", (urlPR,))
		for result in self.cursor.fetchall():
			retorno = result[0]

		return retorno

	def getProjeto(self, link):
		replace = link.replace("https://github.com/", "")
		aux = replace.split("/")
		return aux[0]+"/"+aux[1]
		

	def ajustar(self, inicio, fim):
		retorno = False;
		linhas = self.cursor.execute("""select urlPR, id from analisegithub4.users_testam where arquivos_encontrados = 1 and arquivos_processados is null and id >= %s and id <= %s limit 100""", (inicio, fim))
		lista = self.cursor.fetchall()

		print("Ajustando: ["+str(len(lista))+"]")

		for prAberto in lista:
			print(prAberto[1])
			qtdCodigo 	= self.getCountSemTeste(prAberto[0])
			qtdTeste 	= self.getCountComTeste(prAberto[0])
			
			temTeste = False
			temCodigo = False

			if qtdTeste > 0:
				temTeste = True

			if qtdCodigo > 0:
				temCodigo = True
			

			projeto = self.getProjeto(prAberto[0])
			self.cursor.execute("""UPDATE analisegithub4.users_testam set hasTest = %s, hasCode = %s, qtdArqTest = %s, qtdArqCode = %s, arquivos_processados = 1, projeto = %s where urlPR = %s""", (temTeste, temCodigo, qtdTeste, qtdCodigo, projeto, prAberto[0] ,) )
			self.conn.commit()




banco = Banco()

while(True):
	banco.ajustar(rangeInicial, rangeFinal)
	time.sleep(1)