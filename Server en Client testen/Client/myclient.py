# python -u C:\PythonScripts\Peer2Peer-Chat\Client\myclient.py
'''
TCP/IP Client and Server
Application name: Peer2Peer Chat
Application version: 1.0
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
server_address = ("LaptopFrans", 10034)
# Connect de socket naar de port waar de server aan het luisteren is
print ("Connecting to %s port %s" % server_address)
sock.connect(server_address)
# Na de connectie is gemaakt, data kan gestuurd worden via de socket met sendall()
# en ontvangen worden met recv(), hetzelfde als in de server
sock.close()