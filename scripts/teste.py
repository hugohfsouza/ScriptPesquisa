import pika
import configparser
import mysql.connector
import time

config = configparser.ConfigParser(allow_no_value=True)
config.read("config.ini")

token = config.get("TOKENS", "token1")
headers = {'Authorization': token,'Accept': 'application/vnd.github.v3+json'}



dbconfig = {
    "host":     config.get("MYSQL", "host"),
    "user":     config.get("MYSQL", "user"),
    "passwd":   config.get("MYSQL", "passwd"),
    "db":       config.get("MYSQL", "db"),
}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor();




connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='usuarios2', auto_delete=False)

while(True):
	cursor.execute("""
				select * from analisegithub4.users u 
	where not exists (select 1 from analisegithub4.users_testam where user = u.user)""")
	listaCompleta = cursor.fetchall();






	for x in listaCompleta:
		channel.basic_publish(exchange='', routing_key='hello', body=x[0])
		print(" [x] Sent '"+str(x[0]))
	
	time.sleep(1)




# connection.close()