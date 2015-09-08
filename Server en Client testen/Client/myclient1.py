# python -u C:\PythonScripts\Peer2Peer-Chat\Client\myclient1.py
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
''' Create a dictionary mapping socket module constants to their names. '''
def get_constants(prefix):
	return dict((getattr(socket, n), n)
		for n in dir(socket)
		if n.startswith(prefix)
		)
families = get_constants("AF_")
types = get_constants("SOCK_")
protocols = get_constants("IPPROTO_")
# Create a TCP/IP socket
sock = socket.create_connection(("localhost", 10000))
print ("Family:", families[sock.family])
print ("Type:", types[sock.type])
print ("Protocol:", protocols[sock.proto])
try:
	# Send data
	message = ("This is the message. It will be repeated")
	print ("Sending %s" % message)
	sock.sendall(bytes(message, "UTF-8"))
	amount_received = 0
	amount_expected = len(message)
	while amount_received < amount_expected:
		data = sock.recv(16)
		amount_received += len(data)
		print ("Received %s" % data)
finally:
	print ("Closing socket.")
	sock.close()