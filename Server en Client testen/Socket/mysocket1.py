# python -u C:\PythonScripts\Peer2Peer-Chat\Socket\mysocket1.py
'''
TCP/IP Client and Server
Application name: Peer2Peer Chat
Application version: 2.0
Author name(s): Frans Tuinstra - frans.tuinstra001@fclive.nl
				Jan Hendrik Haanstra(test subject)
1. This program, based on the one in the standard library documentation,
receives incoming messages and echos them back to the sender.
'''
import socket
import sys

# Maakt een TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind de socket aan de port
server_name = (socket.gethostname())
server_address = (server_name, 10000)
print ("Starting up on %s port %s" % server_address)
# De bind() is gebruikt om de socket met de server address vast te maken
sock.bind(server_address)
# Nu zetten we de socket in server mode
sock.listen(1)
while True: # Oneindige loop
	print ("Waiting for a connection...")
	connection, client_adress = sock.accept()
	# accept() Geeft een open connectie van server en client (met address van client)
	# terug, De connectie is een andere socket op een andere port. Data is gelezen door
	# recv() en doorgegeven met sendall()
	try:
		print ("Client connected:", client_adress)
		while True:
			data = connection.recv(1024)
			print ("Received %s" % data)
			if data:
				print ("Sending data back to client...")
				connection.sendall(data)
			else:
				print ("No more data from", client_adress)
				break
	finally:
		connection.close()