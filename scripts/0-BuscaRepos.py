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
  search(query: "is:public language:Java fork:false mirror:false archived:false stars:>2000", type: REPOSITORY, first: 100, after: "#page#") {
    repositoryCount
    pageInfo {
      endCursor
      startCursor
      hasNextPage
    }
    edges {
      node {
        ... on Repository {
          name
          nameWithOwner
          url
          isFork
          createdAt
          databaseId
          id
          languages(orderBy: {field: SIZE, direction: DESC}, first: 20) {
            edges {
              node {
                name
              }
            }
            totalCount
          }
        }
      }
    }
  }
}"""


def requisitarGithub(page):
	global queryInit;
	
	query 	= queryInit.replace('#page#', page)
	request = requests.post('https://api.github.com/graphql',json={'query': query}, headers=headers)
	
	if request.status_code == 200:
		return request.json()
	else:
		raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def busca(pagina):
	lista = []
	return lista
	pass





def insertTabelaControle(startCursor, endCursor):
	global conn
	global cursor
	
	cursor.execute("""INSERT INTO controle (startCursor, endCursor) VALUES (%s, %s)""", (startCursor, endCursor) )
	conn.commit() 


def insertRepositorio(name, nameWithOwner, createdAt, databaseId, languages):
	global conn
	global cursor

	cursor.execute(
		"""insert into repositorios(name, nameWithOwner, createdAt, databaseId,  languages) values (%s, %s, %s, %s, %s)""", (name, nameWithOwner, createdAt, databaseId, languages) )
	conn.commit() 

def verificarUsoApiGithub():
    url = "https://api.github.com/rate_limit"
    response = requests.get(url, headers=headers)
    y = json.loads(response.text)
    print("[Max Reqs] "+str(y["resources"]["graphql"]['remaining']))



endCursor = 'Y3Vyc29yOjEwMA=='

lista 	= requisitarGithub(endCursor)
hasNextPage = True
countTestMacro = 0

while(hasNextPage):
	totalSessao = 0;
	endCursor 	= lista['data']['search']['pageInfo']['endCursor']
	startCuror 	= lista['data']['search']['pageInfo']['startCursor']
	hasNextPage = lista['data']['search']['pageInfo']['hasNextPage']

	print("---------------------------")
	print("endCursor: "+str(endCursor))
	print("startCuror: "+str(startCuror))
	print("hasNextPage: "+str(hasNextPage))
	print("---------------------------")

	insertTabelaControle(startCuror, endCursor)

	for repo in lista['data']['search']['edges']:
		if(not repo['node']['isFork']):
			totalSessao += 1
			stringLinguagens = ""
			for linguagem in repo['node']['languages']['edges']:
				stringLinguagens  += ","+linguagem['node']['name']
			stringLinguagens = stringLinguagens[1:]
				
			countTestMacro += 1
			insertRepositorio(
				repo['node']['name'],
				repo['node']['nameWithOwner'],
				repo['node']['createdAt'],
				repo['node']['databaseId'],
				stringLinguagens
			)
	if(hasNextPage):
		lista 	= requisitarGithub(endCursor)
	verificarUsoApiGithub()
	print("totalSessao: "+str(totalSessao))


print(countTestMacro)