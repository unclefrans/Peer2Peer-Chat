#!/usr/bin/python
#python -u C:\PythonScripts\Peer2Peer-Chat\TweeinEen\testt.py
import threading
import time
import socket
import select
import sys

running = True
backlog = 5
size = 1024
#------------------------------------------------------------
def handler_thread(socket):
#------------------------------------------------------------
	print("Received message: "+socket.recv(1024).decode())
	socket.close()
#End handler_thread

#------------------------------------------------------------
def Connect():
#------------------------------------------------------------
	my_server_host = socket.gethostname()
	my_server_port = 5000
	my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	my_server.connect((my_server_host, my_server_port))
#End of connect to server method

#------------------------------------------------------------
def UI():
#------------------------------------------------------------
	global running
	while(running):
		data = input("[1]Send message\n[2]Exit client\nEnter choice: ")
		if(data.strip() == "1"):
			client_msg = input("Input message: ")
			Connect()
			my_server.send(client_msg.encode())
			my_server.close()
		elif(data.strip() == "2"):
			Connect()
			my_server.close()
			running = False
			sys.exit()
		print("\n")
#End of UI method

#------------------------------------------------------------
def p2p():
#------------------------------------------------------------
	my_server_host = socket.gethostname()
	my_server_port = 5000
	my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	my_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	my_server.bind((my_server_host, my_server_port))
	threading.Thread(target=UI).start()
	my_server.listen(backlog)
	read_list = [my_server]
	while(running):
		readable, writable, errored = select.select(read_list, [], [])
		for s in readable:
			if s is my_server:
				client, client_address = my_server.accept()
				read_list.append(client)
				print("Connection from", client_address)
	print("Closing server")
	my_server.close()
#End of p2p method.

p2p()