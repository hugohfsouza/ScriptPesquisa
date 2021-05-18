import mysql.connector
import json
from prettytable import PrettyTable
import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


tabelaResultado = PrettyTable([
	'Repositorio',
	'Total Contribuidores',
	'Qtd. Pessoas So Testam', 
	'Qtd Pessoas So Code', 
	'Qtd Pessoa Faz os 2'
	# 'Lista Pessoas que só testa', 
	# 'Lista pessoas que so desenvolve', 
	# 'Lista Pessoas que faz os 2', 
	# '% de PR com testes',
	# '% de PRs sem teste'
	])


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

	def listaRepos(self):
		linhas = self.cursor.execute("""SELECT id, nameWithOwner from repositorios where temTeste = 1 and prs_recuperados = 1""")
		return self.cursor.fetchall()

	def getPessoasRepositorio(self, repo_id):
		linhas = self.cursor.execute("""select distinct user from pull_requests where repo_id = %s""", (repo_id,))
		return self.cursor.fetchall()

	def getInfoPRs(self, repo):
		pessoasSoTestam 	= []
		pessoasSoCodificam 	= []
		pessoasFazemOsDois  = []
		totalContribuidores = 0

		query = """ 
				SELECT pr.user, sum(pr.hasTest) as qtdTest, sum(pr.hasCode) as qtdCode from pull_requests as pr
				where pr.repo_id = %s
			    group by pr.user """

		self.cursor.execute(query, (repo[0],))
		resultFetch = self.cursor.fetchall()
		
		totalContribuidores = len(resultFetch)
		for result in resultFetch:
			if(result[1] > 0 and result[2] <= 0):
				pessoasSoTestam.append(result[0])

			if(result[1] <= 0 and result[2] > 0):
				pessoasSoCodificam.append(result[0])

			if(result[1] > 0 and result[2] > 0):
				pessoasFazemOsDois.append(result[0])

		return pessoasSoTestam, pessoasSoCodificam, pessoasFazemOsDois, totalContribuidores
		




banco = Banco()
listaRepositorios = banco.listaRepos()
print('Repositorio|Total Contribuidores|Qtd. Pessoas So Testam|Qtd Pessoas So Code|Qtd Pessoa Faz os 2')
for repo in listaRepositorios:

	pessoasSoTestam, pessoasSoCodificam, pessoasFazemOsDois, totalContribuidores = banco.getInfoPRs(repo)
	print(str(repo[1])+"|"+str(totalContribuidores)+"|"+str(len(pessoasSoTestam))+"|"+str(len(pessoasSoCodificam))+"|"+str(len(pessoasFazemOsDois))  )