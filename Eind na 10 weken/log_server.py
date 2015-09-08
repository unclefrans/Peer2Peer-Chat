# Imports
import os
import sys
import datetime

def connections_queue(myReceiver):
	connections_path = ("Server_logs")
	connections_listCount = (len(myReceiver.connections_list))
	if (connections_listCount != 0):
		if not os.path.exists(connections_path):
			os.makedirs(connections_path)
		today = datetime.date.today()
		connections_filename = (str(today.strftime("%d-%m-%Y"))+".txt")	
		with open(os.path.join(connections_path, connections_filename), "a+") as temp_file:
			for i in myReceiver.connections_list:
				temp_file.write(str(i)+"\n")
			temp_file.write("---------------------------------\n")
		myReceiver.connections_list.clear()