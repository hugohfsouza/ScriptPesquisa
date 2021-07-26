import requests
import json
import time
import mysql.connector
import configparser
import pika, sys, os
import random


config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")


dbconfig = {
    "host":     config.get("MYSQL", "host"),
    "user":     config.get("MYSQL", "user"),
    "passwd":   config.get("MYSQL", "passwd"),
    "db":       "analisegithub5",
}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor();
  
def listToString(s): 
    str1 = "" 
    for ele in s: 
        str1 += ele  
    return str1 


# cursor.execute("update analisegithub5.repositorios_selecionados set prs_recuperadas = 1 where id = %s",(idNovo,) )
# conn.commit()

cursor.execute("select distinct user from teste")
listaUsuarios = cursor.fetchall();

for user in listaUsuarios:
  cursor.execute("""select * from teste where user = %s""", (user[0],) )
  listaProjetos = cursor.fetchall();

  linguagensQueContribui    = []
  acoesEmProjetosDiferentes = []

  for proj in listaProjetos:
    linguagensQueContribui.append(","+proj[2])

    if(proj[3] == 0 and proj[4] >= 1  ):
        acoesEmProjetosDiferentes.append(",Codigo")

    if(proj[3] >= 1 and proj[4] >= 1  ):
        acoesEmProjetosDiferentes.append(",CodigoTeste")

    if(proj[3] >= 1 and proj[4] == 0  ):
        acoesEmProjetosDiferentes.append(",Teste")

  print(f"{user[0]}|{len(listaProjetos)}|{listToString(set(linguagensQueContribui))}|{listToString(set(acoesEmProjetosDiferentes))}")


