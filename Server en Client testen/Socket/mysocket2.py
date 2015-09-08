# python -u C:\PythonScripts\Peer2Peer-Chat\Socket\mysocket2.py
import socket
import sys
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (socket.gethostname(), 10000)
sock.bind(server_address)
print ("Starting up on %s port %s" % sock.getsockname())
sock.listen(1)
while True:
	print ("Waiting for connection.")
	connection, client_address = sock.accept()
	try:
		print ("Client connected:", client_address)
		while True:
			data = connection.recv(16)
			print ("Received %s" % data)
			if data:
				connection.sendall(data)
			else:
				break
	finally:
		connection.close()