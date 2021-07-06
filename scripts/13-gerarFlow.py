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

dadosGeraisFluxo = []


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


	def ver(self, linguagem):
		global dadosGeraisFluxo
		self.cursor.execute("""
				SELECT 
				    historico
				from users_consolidado""")
		listaCompleta = self.cursor.fetchall();
		for flow in listaCompleta:
			arrayFlow = flow[0][1::].split(",")
			
			for x in range(len(arrayFlow)-1):
				# print(arrayFlow[x] + "  " + arrayFlow[x+1])
				dadosGeraisFluxo.append( (arrayFlow[x], arrayFlow[x+1]))

		self.agruparEContar(dadosGeraisFluxo, linguagem)

	def agruparEContar(self, arrayFlow, linguagem):
		
		for x in arrayFlow:
			string = x[0]+"->"+x[1]
			self.cursor.execute("""INSERT INTO analisegithub.flow_consolidado VALUES (%s,%s,%s,%s);""", (linguagem, x[0], x[1], string ))
			self.conn.commit()
			# print(f"{linguagem};{x[0]};{x[1]};{x[0]}->{x[1]} " )
			# pass

bancoJava = Banco("analisegithub")
bancoJava.ver("java")

bancoJavascript = Banco("analisegithub2")
bancoJavascript.ver("javascript")

bancoPython = Banco("analisegithub3")
bancoPython.ver("python")