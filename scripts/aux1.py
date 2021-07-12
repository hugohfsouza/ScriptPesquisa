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
  




def recuperaInfosJava(idNovo, repo):
  
  cursor.execute("select id from analisegithub.repositorios where nameWithOwner like %s and temTeste = 1", (repo,))
  registroIdRepo = cursor.fetchone()
  print(registroIdRepo)
  if(registroIdRepo):
    sqlRecupera = """
      INSERT into analisegithub5.pull_requests(
        repo_id, 
        number,
        state,
        url,
        user,
        created_at,
        updated_at,
        closed_at,
        merged_at,
        hasTest,
        hasCode,
        qtdArqTest,
        qtdArqCode,
        qtdAdditions, 
        qtdDeletions)
      SELECT %s, number, state, url, user, created_at, updated_at, closed_at, merged_at, hasTest, hasCode, qtdArqTest, qtdArqCode, qtdAdditions, qtdDeletions  from analisegithub.pull_requests pr
          where pr.repo_id = %s
    """
    cursor.execute(sqlRecupera, (idNovo,registroIdRepo[0]))
    conn.commit()

    cursor.execute("update analisegithub5.repositorios_selecionados set prs_recuperadas = 1 where id = %s",(idNovo,) )
    conn.commit()



def recuperaInfosJavascript(idNovo, repo):
  
  cursor.execute("select id from analisegithub2.repositorios where nameWithOwner like %s and temTeste = 1", (repo,))
  registroIdRepo = cursor.fetchone()
  print(registroIdRepo)
  if(registroIdRepo):
    sqlRecupera = """
      INSERT into analisegithub5.pull_requests(
        repo_id, 
        number,
        state,
        url,
        user,
        created_at,
        updated_at,
        closed_at,
        merged_at,
        hasTest,
        hasCode,
        qtdArqTest,
        qtdArqCode,
        qtdAdditions, 
        qtdDeletions)
      SELECT %s, number, state, url, user, created_at, updated_at, closed_at, merged_at, hasTest, hasCode, qtdArqTest, qtdArqCode, qtdAdditions, qtdDeletions  from analisegithub2.pull_requests pr
          where pr.repo_id = %s
    """
    cursor.execute(sqlRecupera, (idNovo,registroIdRepo[0]))
    conn.commit()

    cursor.execute("update analisegithub5.repositorios_selecionados set prs_recuperadas = 1 where id = %s",(idNovo,) )
    conn.commit()




def recuperaInfosPython(idNovo, repo):
  
  cursor.execute("select id from analisegithub3.repositorios where nameWithOwner like %s and temTeste = 1", (repo,))
  registroIdRepo = cursor.fetchone()
  print(registroIdRepo)
  if(registroIdRepo):
    sqlRecupera = """
      INSERT into analisegithub5.pull_requests(
        repo_id, 
        number,
        state,
        url,
        user,
        created_at,
        updated_at,
        closed_at,
        merged_at,
        hasTest,
        hasCode,
        qtdArqTest,
        qtdArqCode,
        qtdAdditions, 
        qtdDeletions)
      SELECT %s, number, state, url, user, created_at, updated_at, closed_at, merged_at, hasTest, hasCode, qtdArqTest, qtdArqCode, qtdAdditions, qtdDeletions  from analisegithub3.pull_requests pr
          where pr.repo_id = %s
    """
    cursor.execute(sqlRecupera, (idNovo,registroIdRepo[0]))
    conn.commit()

    cursor.execute("update analisegithub5.repositorios_selecionados set prs_recuperadas = 1 where id = %s",(idNovo,) )
    conn.commit()

cursor.execute("select id, nameWithOwner, linguagemPrincipal from analisegithub5.repositorios_selecionados where prs_recuperadas is null")
listaRepositorios = cursor.fetchall();

for repo in listaRepositorios:
  print(repo[2])
  if(repo[2] == 'Java'):
    recuperaInfosJava(repo[0], repo[1])

  if(repo[2] == 'Javascript'):
    recuperaInfosJavascript(repo[0], repo[1])

  if(repo[2] == 'Python'):
    recuperaInfosPython(repo[0], repo[1])


