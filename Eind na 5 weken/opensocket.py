# python -u C:\PythonScripts\LaatsteWeek\opensocket.py
'''
Testing for main.py
Opening a socket for main.py to connect to
'''
import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = socket.gethostname()
port = 8890

sock.bind((address, port))
print ("Starting up on %s port %s" % sock.getsockname())
sock.listen(1)
while True:
	print ("Waiting for connection.")
	connection, client_address = sock.accept()
	try:
		print ("Client connected:", client_address)
		while True:
			data = connection.recv(256)
			if data:
				msg = str(data)
				filename = ("test.txt") # The name of the file to write in
				try: # Try opening the file...
					f = (open(filename, "w+")) # ...and write it, set it as f
					f.write(msg)
					f.close() # ALWAYS CLOSE THE FILE IF YOU'VE OPENED IT!
				finally:
					f = (open(filename, "r+")) # ...and read it, set it as f
					with open(filename) as my_file: # This whole thing
						my_file.seek(0) # Start looking
						first_char = my_file.read(1) # Read on the next line
						if 'Profile:' in open(filename, "r+").read():
							for line in f:
								profile_name = line.split(",")[1]
								profile_ip = line.split(",")[2]
								profile_port = line.split(",")[3]			
							#print(
							#	profile_name + "," +
							#	profile_ip + ":" +
							#	profile_port
							#	)
							connection.sendall(data)
							f.close()
							break
						else:
							f.close()
							connection.sendall(bytes("No", "UTF-8"))
							break
	finally:
		#print("Closing Socket")
		connection.close()
sock.close()