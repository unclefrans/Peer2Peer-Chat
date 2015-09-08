# python -u C:\PythonScripts\NieuwsteVersie\f1.py
'''
TCP/IP Client and Server
Application name: Peer2Peer Chat
Application version: 2.0
Author name(s): Frans Tuinstra - frans.tuinstra001@fclive.nl
'''
# Imports
import time

# Import local files
import profile
myProfile = profile.MainClass()
import receiver
myReceiver = receiver.MainClass(0, 0) # Begins the receiver socket

loop = True
while(loop):
	from log_server import connections_queue
	connections_queue(myReceiver)
	time.sleep(5)

'''
main
start thread server(ontvanger)
start queue thread
start thread client
start thread sender(verstuurder)
'''