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
    "db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor();
  



# cursor.execute("update analisegithub5.repositorios_selecionados set prs_recuperadas = 1 where id = %s",(idNovo,) )
# conn.commit()

cursor.execute("select id, nameWithOwner, linguagemPrincipal from analisegithub5.repositorios_selecionados")
listaRepositorios = cursor.fetchall();

for repo in listaRepositorios:

  cursor.execute("select count(1) from analisegithub5.pull_requests where repo_id = %s", (repo[0],) )
  registroQuantidade = cursor.fetchone();
  if(registroQuantidade):
    cursor.execute("update analisegithub5.repositorios_selecionados set qtdPRsRecuperadas = %s where id = %s", (registroQuantidade[0], repo[0]))
    conn.commit()



