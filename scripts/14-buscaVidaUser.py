import requests
import json
import time
import mysql.connector
import configparser

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

token = config.get("TOKENS", "token1")


dbconfig = {
    "host":     config.get("MYSQL", "host"),
    "user":     config.get("MYSQL", "user"),
    "passwd":   config.get("MYSQL", "passwd"),
    "db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor();


headers = {'Authorization': token,'Accept': 'application/vnd.github.v3+json'}


queryInit = """ 
{
  user(login: "#user#") {
    id
    pullRequests(first: 100) {
      pageInfo {
        hasNextPage
        hasPreviousPage
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

	request = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)
	
	if request.status_code == 200:
		return request.json()
	else:
		raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))



user = "igorsteinmacher"
user = "0dvictor"



retorno = requisitarGithub(user)
print(user)
print(retorno["data"]["user"]["id"])
print(retorno["data"]["user"]["pullRequests"]["totalCount"])

print("--------")
for x in retorno["data"]["user"]["pullRequests"]["edges"]:
	# print(x["node"]["merged"])
	print(x["node"]["url"])
	print("--------")
