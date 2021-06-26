import mysql.connector
import json
import time
import configparser
import sys
import requests
import json
import time
import mysql.connector

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")



token 	= config.get("TOKENS", sys.argv[1])
headers	= {'Authorization': token}

rangeInicial 	= sys.argv[2]
rangeFinal 		= sys.argv[3]

class Banco():

	def __init__(self):
		dbconfig = {
			"host":     config.get("MYSQL", "host"),
		    "user":     config.get("MYSQL", "user"),
		    "passwd":   config.get("MYSQL", "passwd"),
		    "db":       config.get("MYSQL", "db"),
		}

		self.conn = mysql.connector.connect(pool_name = "mypool", pool_size = 10,**dbconfig)
		self.cursor = self.conn.cursor();

	def requisitarGithub(self, url, headerExtra=None):	 
		response = requests.get(url, headers=headers)
		return json.loads(response.text)

	def ajustar(self, inicio, fim):
		
		self.cursor.execute("""
				SELECT github_id, url from 
					pull_requests 
				where repo_id in (1856,1935,1827,1826,1968,2418,1961,2189,2057,1812,1978,2645,2334,1807,1905,2417,1833,2029,1861,1880,1917,2012,2257,1883,1950,2458,2391,1824,1965,2559)
				and repo_id >= %s
                and repo_id <= %s
                and state <> 'open'
				and closed_at is null;
			""", (inicio, fim))


		for prAberto in self.cursor.fetchall():
			retorno = self.requisitarGithub(prAberto[1])
			banco.atualizaPr(retorno['id'], retorno['closed_at'], retorno['merged_at'])
			pass


	def atualizaPr(self, idGithub, closed_at, merged_at):
		self.cursor.execute(""" UPDATE pull_requests set closed_at = %s, merged_at = %s where github_id = %s""", (closed_at, merged_at, idGithub  ) )
		self.conn.commit()


		


banco = Banco()

# while(True):
banco.ajustar(rangeInicial, rangeFinal)
