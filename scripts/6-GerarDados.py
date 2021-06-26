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
		# linhas = self.cursor.execute("""SELECT id, nameWithOwner from repositorios where id in (1657,1432,1231,1750,1190,1286,909,1549,982,1032,1371,987,1215,1716,1080,928,1010,1504,1094,1559,991,1384,1486,1000,1129,1727,1303,919,901,1174)""")
		# linhas = self.cursor.execute("""SELECT id, nameWithOwner from repositorios where id in (1842,2085,1985,2479,2113,1839,1899,2356,1895,2499,2333,1933,1939,1989,2122,2324,1827,2409,1996,1814,1867,2539,2007,2291,2000,2247,2156,2051,2112,2592)""")
		# linhas = self.cursor.execute("""SELECT id, nameWithOwner from repositorios where id in (1856,1935,1827,1826,1968,2418,1961,2189,2057,1812,1978,2645,2334,1807,1905,2417,1833,2029,1861,1880,1917,2012,2257,1883,1950,2458,2391,1824,1965,2559)""")
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

	def getInfoPRsMerged(self, repo):
		query = """ 
				SELECT
					(select count(1) from pull_requests pr1 where pr1.repo_id = %s and hasTest = 1 and hasCode = 0) qtdPRsApenasComTeste,
				    (select count(1) from pull_requests pr1 where pr1.repo_id = %s and hasTest = 1 and hasCode = 0 and merged_at is not null) qtdPRsApenasComTestePRAceito,
				    (select count(1) from pull_requests pr1 where pr1.repo_id = %s and hasTest = 0 and hasCode = 1) qtdPRsApenasComCodigo,
				    (select count(1) from pull_requests pr1 where pr1.repo_id = %s and hasTest = 0 and hasCode = 1 and merged_at is not null) qtdPRsApenasComCodigoPRAceito,
				    (select count(1) from pull_requests pr1 where pr1.repo_id = %s and hasTest = 1 and hasCode = 1) qtdPRsComCodigoETeste,
				    (select count(1) from pull_requests pr1 where pr1.repo_id = %s and hasTest = 1 and hasCode = 1 and merged_at is not null) qtdPRsComCodigoETesteComPRAceito,
				    (select count(1) from pull_requests pr1 where pr1.repo_id = %s) totalPRs
				from dual"""
		self.cursor.execute(query, (repo[0],repo[0],repo[0],repo[0],repo[0],repo[0],repo[0]))
		resultFetch = self.cursor.fetchone()

		resultado = {
			'qtdPRsApenasComTeste': resultFetch[0],
			'qtdPRsApenasComTestePRAceito': resultFetch[1],
			'qtdPRsApenasComCodigo': resultFetch[2],
			'qtdPRsApenasComCodigoPRAceito': resultFetch[3],
			'qtdPRsComCodigoETeste': resultFetch[4],
			'qtdPRsComCodigoETesteComPRAceito': resultFetch[5],
			'totalPRs': resultFetch[6],
		}

		return resultado




def montaStringPessoa(arrayPessoa):
	retorno = ""
	for x in arrayPessoa:
		retorno += ", "+x

	return retorno[1:]


banco = Banco()
listaRepositorios = banco.listaRepos()
print('Repositorio|Total Contribuidores|Qtd. Pessoas Contribuiem apenas com teste|Qtd. Pessoas Contribuiem apenas com produto|Qtd. Pessoas Contribuiem produto e teste|qtdPRsApenasComTeste|qtdPRsApenasComTestePRAceito|qtdPRsApenasComCodigo|qtdPRsApenasComCodigoPRAceito|qtdPRsComCodigoETeste|qtdPRsComCodigoETesteComPRAceito|totalPRs')
for repo in listaRepositorios:

	pessoasSoTestam, pessoasSoCodificam, pessoasFazemOsDois, totalContribuidores = banco.getInfoPRs(repo)
	analiseMerged = banco.getInfoPRsMerged(repo)

	print(
		str(repo[1])+"|"
		+str(totalContribuidores)+"|"
		+str(len(pessoasSoTestam))+"|"
		+str(len(pessoasSoCodificam))+"|"
		+str(len(pessoasFazemOsDois))+"|"
		+str(analiseMerged['qtdPRsApenasComTeste'])+"|"
		+str(analiseMerged['qtdPRsApenasComTestePRAceito'])+"|"
		+str(analiseMerged['qtdPRsApenasComCodigo'])+"|"
		+str(analiseMerged['qtdPRsApenasComCodigoPRAceito'])+"|"
		+str(analiseMerged['qtdPRsComCodigoETeste'])+"|"
		+str(analiseMerged['qtdPRsComCodigoETesteComPRAceito'])+"|"
		+str(analiseMerged['totalPRs'])
	)



