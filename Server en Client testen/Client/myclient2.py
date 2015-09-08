# python -u C:\PythonScripts\Peer2Peer-Chat\Client\myclient2.py
'''
TCP/IP Client and Server
Application name: Peer2Peer Chat
Application version: 3.0
Author name(s): Frans Tuinstra - frans.tuinstra001@fclive.nl
				Jan Hendrik Haanstra(test subject)
1. This program, based on the one in the standard library documentation,
receives incoming messages and echos them back to the sender.
'''
import socket
import sys
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port on the server given by the caller
HOST = "LaptopFrans"
PORT = 10034

#server_address = ("Jelle", 8881)
#print ('connecting to %s port %s' % server_address)
sock.connect((HOST,PORT))
try:
    message = 'This is the message.  It will be repeated.'
    print ('sending "%s"' % message)
    sock.sendall(bytes(message, "UTF-8"))
    amount_received = 0
    amount_expected = len(message)
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print ('received "%s"' % data)
        #input()
finally:
    print ("Socket closed.")
    sock.close()