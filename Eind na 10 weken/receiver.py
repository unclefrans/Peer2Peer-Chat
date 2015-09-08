# Module: Receiver

# Imports
import socket
import threading
import datetime
from time import localtime, strftime

class MainClass(object):
	def __init__(self, connectionMessage, connections_list):
		self.connections_list = []
		threading.Thread(target=self.server_StartListening).start()
	def get_connectionMessage(self):
		return(self.connectionMessage)
	def set_connectionMessage(self, connectionMessage):
		self.connectionMessage = (connectionMessage)
	def print_connectionMessage(self):
		print(self.connectionMessage)
	def server_StartListening(self):	
		address = (socket.gethostname())
		port = (10034)
		sock = (socket.socket(socket.AF_INET, socket.SOCK_STREAM))
		sock.bind((address, port))
		sock.listen(1)
		while(True):
			connection, client_address = (sock.accept())
			connectionMessage = ((client_address))
			self.set_connectionMessage(connectionMessage)
			current_time = strftime("%H:%M:%S", localtime())
			self.connections_list.append(
				str(current_time) + 
				" - " +
				str((connectionMessage)))
			#return((self.connectionMessage))
		sock.close()