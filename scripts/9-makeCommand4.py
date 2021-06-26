import mysql.connector
import json
import configparser
import os

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


dbconfig = {
    "host":     config.get("MYSQL", "host"),
    "user":     config.get("MYSQL", "user"),
    "passwd":   config.get("MYSQL", "passwd"),
    "db":       config.get("MYSQL", "db"),
}

totalTokens = 4

conn = mysql.connector.connect(pool_name = "mypool", pool_size = 1,**dbconfig)
cursor = conn.cursor();



# Recuperar PRs
# cursor.execute("""SELECT count(1) from repositorios where temTeste is not null""")
# total =  cursor.fetchone()
 

# qtdPorComando 	= int(total[0]/(totalTokens*2))
# idMinimoAtual 	= 0;
# ultimoId 		= 0;

# while(idMinimoAtual < total[0]):
	
# 	idPrimeiro 	= 0;
# 	idUltimo 	= 0;
# 	i 			= True;

# 	cursor.execute("""
# 		SELECT id from repositorios where temTeste is not null and id > %s order by id limit %s 
# 		""", (ultimoId, qtdPorComando))

# 	for linha in cursor.fetchall():
# 		if(i == True):
# 			i = False
# 			idPrimeiro = linha[0]

# 		idUltimo = linha[0]

# 	ultimoId = idUltimo
# 	print("python .\\2-buscaListaPrs.py token1 ", idPrimeiro, idUltimo)


# 	idMinimoAtual += qtdPorComando;




# RECUPERA ARQUIVOS
cursor.execute("""
	SELECT count(1) from repositorios as a
                    inner join pull_requests as b on (a.id = b.repo_id)
                    where a.temTeste = 1
                    and a.prs_recuperados = 1
                    and b.pr_analisado = 0
                    and a.id in (1842,2085,1985,2479,2113,1839,1899,2356,1895,2499,2333,1933,1939,1989,2122,2324,1827,2409,1996,1814,1867,2539,2007,2291,2000,2247,2156,2051,2112,2592)
	""")
total =  cursor.fetchone()
 

qtdPorComando 	= int(total[0]/(totalTokens*2))
idMinimoAtual 	= 0;
ultimoId 		= 0;

while(idMinimoAtual < total[0]):
	
	idPrimeiro 	= 0;
	idUltimo 	= 0;
	i 			= True;

	cursor.execute("""
		SELECT b.* from repositorios as a
                    inner join pull_requests as b on (a.id = b.repo_id)
                    where a.temTeste = 1
                    and a.prs_recuperados = 1
                    and b.pr_analisado = 0
                    and a.id in (1842,2085,1985,2479,2113,1839,1899,2356,1895,2499,2333,1933,1939,1989,2122,2324,1827,2409,1996,1814,1867,2539,2007,2291,2000,2247,2156,2051,2112,2592)
                    and b.id > %s
                    order by id
                    limit %s
		""", (ultimoId, qtdPorComando))

	for linha in cursor.fetchall():
		if(i == True):
			i = False
			idPrimeiro = linha[0]

		idUltimo = linha[0]

	ultimoId = idUltimo
	print("python .\\4-recuperaArquivosPR.py token1 ", idPrimeiro, idUltimo)


	idMinimoAtual += qtdPorComando;











# python .\4-recuperaArquivosPR.py token1 502761 554960
# python .\4-recuperaArquivosPR.py token1 554961 588566

# python .\4-recuperaArquivosPR.py token2 588567 633708
# python .\4-recuperaArquivosPR.py token2 633709 690948


# python .\4-recuperaArquivosPR.py token3 690950  743246
# python .\4-recuperaArquivosPR.py token3  743247  847815

# python .\4-recuperaArquivosPR.py token4 847816  957410
# python .\4-recuperaArquivosPR.py token4  957411  1015721