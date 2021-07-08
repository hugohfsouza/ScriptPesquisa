import requests
import json
import time
import mysql.connector
import configparser
import pika, sys, os
import random


config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

token = config.get("TOKENS", "token1")

configuracao  = config.items("TOKENS")
tokens = []
for x in configuracao:
  tokens.append(x[1])



headers = {'Authorization': token,'Accept': 'application/vnd.github.v3+json'}



dbconfig = {
    "host":     config.get("MYSQL", "host"),
    "user":     config.get("MYSQL", "user"),
    "passwd":   config.get("MYSQL", "passwd"),
    "db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor();





queryInit = """ 
{
  user(login: "#user#") {
    id
    pullRequests(first: 100, orderBy: {field: CREATED_AT, direction: ASC}, after: "#page#") {
      pageInfo {
        hasNextPage
        hasPreviousPage
        startCursor
      }
      totalCount
      edges {
        node {
          id
          merged
          url
        }
      }
    }
  }
}

"""


def requisitarGithub(user):
  global queryInit;

  query 	= queryInit.replace('#user#', user)
  query   = query.replace(', after: "#page#"', '')
  todosOsRequests = []

  headers = {'Authorization': random.choice(tokens),'Accept': 'application/vnd.github.v3+json'}


  request = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)
  result = request.json()

  print(request.status_code)

  todosOsRequests.append(result)
  if(result["data"]["user"]):
    while(result["data"]["user"]["pullRequests"]["pageInfo"]["hasNextPage"]):
      query   = queryInit.replace('#user#', user)
      query   = query.replace('#page#', result["data"]["user"]["pullRequests"]["pageInfo"]["startCursor"])
      request = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)
      result = request.json()
      todosOsRequests.append(result)

  return todosOsRequests


def processar(user):
  print("fazendo: "+str(user))
  # try:
  retorno = requisitarGithub(user)
  for lis in retorno:
    if(lis["data"]["user"]):
      for x in lis["data"]["user"]["pullRequests"]["edges"]:
        try:
          cursor.execute("""insert into analisegithub4.users_testam(user, urlPR, merged) values (%s,%s,%s)""", (user, x["node"]["url"],x["node"]["merged"]) )
          conn.commit()
        except Exception as e:
          pass  
  # except Exception as e:
  #   print(e)
  




def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='usuarios2', auto_delete=False)


    def callback(ch, method, properties, body):
      processar(body.decode('ascii'))


    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=False)
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
