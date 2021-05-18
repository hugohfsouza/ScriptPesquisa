import mysql.connector
import json
import time
import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

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

	def getCountComTeste(self, pr_id):
		retorno = 0
		linhas = self.cursor.execute("""SELECT count(1) from pull_request_files where pr_id = %s and filename like '%test%'""", (pr_id,))
		for result in self.cursor.fetchall():
			retorno = result[0]

		return retorno

	def getCountSemTeste(self, pr_id):
		retorno = 0;
		linhas = self.cursor.execute("""SELECT count(1) from pull_request_files where pr_id = %s and filename not like '%test%'""", (pr_id,))
		for result in self.cursor.fetchall():
			retorno = result[0]

		return retorno

	def ajustar(self):
		retorno = False;
		linhas = self.cursor.execute("""SELECT * from pull_requests where pr_analisado = 1 and hasTest is null""")
		lista = self.cursor.fetchall()

		print("Ajustando: ["+str(len(lista))+"]")

		for prAberto in lista:
			qtdCodigo 	= self.getCountSemTeste(prAberto[0])
			qtdTeste 	= self.getCountComTeste(prAberto[0])
			
			temTeste = False
			temCodigo = False

			if qtdTeste > 0:
				temTeste = True

			if qtdCodigo > 0:
				temCodigo = True
			
			self.cursor.execute("""UPDATE pull_requests set hasTest = %s, hasCode = %s, qtdArqTest = %s, qtdArqCode = %s where id = %s""", (temTeste, temCodigo, qtdTeste, qtdCodigo, prAberto[0] ,) )
			self.conn.commit()

	def ajustarAdditionsDeletions(self):
		linhas = self.cursor.execute("""SELECT id from pull_requests where pr_analisado = 1 and qtdAdditions is null""")
		lista = self.cursor.fetchall()


		for pr in lista:
			resul = self.cursor.execute("""select sum(additions), sum(deletions) from pull_request_files where pr_id = %s""", (pr[0],));
			result = self.cursor.fetchone()
			
			self.cursor.execute("""UPDATE pull_requests set qtdAdditions = %s, qtdDeletions = %s where id = %s""", (result[0], result[1], pr[0], ) )
			self.conn.commit()



banco = Banco()

while(True):
	banco.ajustar()
	# banco.ajustarAdditionsDeletions()
	time.sleep(120)