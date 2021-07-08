import mysql.connector
import json
import time
import configparser
import sys
import requests
import mysql.connector
from alive_progress import alive_bar



config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")



class Banco():

	def __init__(self, database):
		dbconfig = {
			"host":     config.get("MYSQL", "host"),
		    "user":     config.get("MYSQL", "user"),
		    "passwd":   config.get("MYSQL", "passwd"),
		    "db":       database,
		}

		self.conn = mysql.connector.connect(pool_name = "mypool", pool_size = 10,**dbconfig)
		self.cursor = self.conn.cursor();

		if(database == 'analisegithub'):
			self.projetos = "1657,1432,1231,1750,1190,1286,909,1549,982,1032,1371,987,1215,1716,1080,928,1010,1504,1094,1559,991,1384,1486,1000,1129,1727,1303,919,901,1174"
			self.linguagem = "Java"

		if(database == 'analisegithub2'):
			self.projetos = "1842,2085,1985,2479,2113,1839,1899,2356,1895,2499,2333,1933,1939,1989,2122,2324,1827,2409,1996,1814,1867,2539,2007,2291,2000,2247,2156,2051,2112,2592"
			self.linguagem = "Javascript"

		if(database == 'analisegithub3'):
			self.projetos = "1856,1935,1827,1826,1968,2418,1961,2189,2057,1812,1978,2645,2334,1807,1905,2417,1833,2029,1861,1880,1917,2012,2257,1883,1950,2458,2391,1824,1965,2559"
			self.linguagem = "Python"



	def getDados(self, user):
		 # DATE_FORMAT(created_at, '%m/%Y'),
		self.cursor.execute("""
				SELECT 
					user, 
				    hasTest,
				    hasCode
				     from pull_requests 
				where repo_id in (""" + self.projetos +""")
				and user = %s 
				order by created_at
			""", (user, ))

		stringHistorico = ""

		interacao 	= 0
		comecouCom 	= ""
		pessoa 		= "";

		lista = self.cursor.fetchall()
		ultimoTipo = ""
		for contrib in lista:
			tipo = "codigoTeste"

			if(contrib[1] == 0 and contrib[2] == 1  ):
				tipo = "codigo"
			
			if (contrib[1] == 1 and contrib[2] == 0 ):
				tipo = "teste"

			if(interacao == 0):
				interacao = 1;
				pessoa = contrib[0]
				comecouCom = tipo
			
			# if(tipo != ultimoTipo):
			stringHistorico += ","+str(tipo)

			# ultimoTipo = tipo


		self.cursor.execute(""" select count(1) from (select distinct repo_id from pull_requests where user = %s) as a """, (user, ))
		quantidadeProjetos = self.cursor.fetchone()


		self.cursor.execute("""
				SELECT count(1) from 
					pull_requests 
						where 
							user = %s
				            and hasTest = 0
				            and hasCode = 1
				            and repo_id in (""" + self.projetos +""")
			""", (user, ))
		resultqtdPRsCodigo = self.cursor.fetchone()

		print(resultqtdPRsCodigo, user);
		exit()
		



		self.cursor.execute("""
				INSERT into users_consolidado 
				values (%s, %s, %s, %s, qtdPRsTeste, qtdPRsCodigoTeste, %s, %s)
			""", (pessoa, quantidadeProjetos[0], len(lista), resultqtdPRsCodigo[0], qtdPRsTeste, qtdPRsCodigoTeste, comecouCom, stringHistorico) )
		self.conn.commit()
		arquivo.write(f"{self.linguagem}|{pessoa}|{comecouCom}|{len(lista)}|{stringHistorico} \n")



	def ver(self):
		self.cursor.execute("""
				SELECT distinct
					pr.user
				from pull_requests pr
				    where pr.repo_id in (""" + self.projetos +""")
				    and (hasCode = 1 or hasTest = 1)
				    order by pr.user
			""")
		listaCompleta = self.cursor.fetchall();
		for pessoa in listaCompleta:
				self.getDados(pessoa[0])
		# with alive_bar(len(listaCompleta)) as bar:
				# bar()


		
print(f"linguagem|usuario|comecouCom|qtdPr")

arquivo = open("java.txt", "a")
bancoJava = Banco("analisegithub")
bancoJava.ver()

# arquivo = open("javascript.txt", "a")
# bancoJavascript = Banco("analisegithub2")
# bancoJavascript.ver()

# arquivo = open("python.txt", "a")
# bancoPython = Banco("analisegithub3")
# bancoPython.ver()