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
  



# cursor.execute("update analisegithub5.repositorios_selecionados set prs_recuperadas = 1 where id = %s",(idNovo,) )
# conn.commit()

cursor.execute("select distinct user from pull_requests")
listaUsuarios = cursor.fetchall();

for user in listaUsuarios:
  cursor.execute("""
    SELECT 
        distinct 
        rs.linguagemPrincipal
    FROM
        pull_requests pr
            INNER JOIN
        repositorios_selecionados rs ON (pr.repo_id = rs.id)
    where user = %s
  """, (user[0],) )
  registroQuantidade = cursor.fetchall();
  linguagensUsuario = ""
  for x in registroQuantidade:
    linguagensUsuario = linguagensUsuario + str(x[0]) + ","

  print(f"{user[0]}|{linguagensUsuario}")


