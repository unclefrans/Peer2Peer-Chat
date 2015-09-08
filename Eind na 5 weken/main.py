'''
TCP/IP Client and Server
Application name: Peer2Peer Chat
Application version: 1.0
Author name(s): Frans Tuinstra - frans.tuinstra001@fclive.nl
				Jan Hendrik Haanstra(collega)
This program should do the following:
1. 	Contact manager
	1.1 Add contacts
	1.2 Edit contacts
	1.3 Remove contacts

2.	Who is online from contact list
	Send pings to existing contacts, try their registered port
	using multiple threads trying to connect to their previous
	registered port +5/-5 around 10 threads running each contact.
	2.1 If connected to wrong person, or failed, try again. 
		If it keeps failing, you should edit this person's 
		contact in the contact manager.
	2.2 If connection successfull, display this user online.
		You're now 'able' to chat with this person.

3. 	(Multiple) Chat screens
4. 	Your own profile
'''
from tkinter import *
import sys
import os
import tkinter.messagebox
import threading
import socket
import select
import random

# ---------------------------------------------------------------------
class MainSystem(object):
# ---------------------------------------------------------------------
	''' The main class, everything that happens will come back to this 
	class, and this class will sends through to other classes what should
	happen. '''

	# -----------------------------------------------------------------
	def __init__(self):
	# -----------------------------------------------------------------
		''' The constructor of the class, prepares the class for use. '''
		self.mainScreen = MainScreen()
		#self.newChat = NewChat()
		#print(self.mainScreen.a) # To test, Show from another class
		mainloop()

# ---------------------------------------------------------------------
class MainScreen(Frame):
# ---------------------------------------------------------------------
	''' Creating the main screen, from top to bottom:
	1. Menu bar
	2. Profile
	3. Online contact(s)
	4. Quit '''

	# -----------------------------------------------------------------
	def __init__(self, parent=None):
	# -----------------------------------------------------------------
		''' The constructor of the class, prepares the class for use. '''
		Frame.__init__(self, parent) # Creates the window
		self.pack() # ?
		self.master.title("Peer2Peer Chat") # Title for window
		self.master.iconname("tkpython") # Icon
		self.master.geometry("400x350+200+200") # Size for window

		self.readProfile() # Reads the profile file

		threading.Thread(target=self.startSocket).start() # Creates the socket to listen for connections
		self.createWidgets() # Create the widgets, to show in window
		#self.a = "b" # To test, Give to other class
		self.start_new_chat = False # If you want to start a new chat

	# -----------------------------------------------------------------
	def readProfile(self):
	# -----------------------------------------------------------------
		filename = ("profile.txt") # The name of the file to read for your profile
		try: # Try opening the file...
			f = (open(filename, "r+")) # ...and read it, set it as read
			with open(filename) as my_file: # This whole thing
				my_file.seek(0) # Start looking
				first_char = my_file.read(1) # Read on the next line
				name = "Frans"
				host = "LaptopFrans"
				port = "10000"
		finally:
			f.close() # ALWAYS CLOSE THE FILE IF YOU'VE OPENED IT!
		self.profile_name = name
		self.profile_ip = host
		self.profile_port = int(port)
		print(self.profile_port)

	# -----------------------------------------------------------------
	def startSocket(self):
	# -----------------------------------------------------------------
		''' Creates the socket to listen for connections '''
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		address = self.profile_ip
		port = int(self.profile_port)

		self.sock.bind((address, port))
		self.sock.listen(1)
		while True:
			print ("Waiting for connection.")
			connection, client_address = self.sock.accept()
			try:
				print ("Client connected:", client_address)
				while True:
					data = connection.recv(256)
					if data:
						filename = ("inc_msg.txt") # The name of the file to write in
						try: # Try opening the file...
							f = (open(filename, "w+")) # ...and write it, set it as f
							f.write(data.decode("UTF-8"))
							#f.write(data)
							f.close() # ALWAYS CLOSE THE FILE IF YOU'VE OPENED IT!
						finally:
							f = (open(filename, "r+")) # ...and read it, set it as f
							with open(filename) as my_file: # This whole thing
								my_file.seek(0) # Start looking
								first_char = my_file.read(1) # Read on the next line
								if 'Profile:' in open(filename, "r+").read(): # If "Profile" was sent then it's a valid connection
									self.new_port = 9999 # Random port
									self.new_port = random.randint(9001,9999) # Random port
									self.new_host = socket.gethostname()
									threading.Thread(target=self.startNewSocket).start() # Opens a new random socket for this connection
									#for line in f:
									#	profile_name = line.split(",")[1]
									#	profile_ip = line.split(",")[2]
									#	profile_port = line.split(",")[3]			
									#print("Socket: " +
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
		self.sock.close()

	# -----------------------------------------------------------------
	def startNewSocket(self):
	# -----------------------------------------------------------------
		''' Starting a new random socket. '''
		self.new_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.new_socket.bind((self.new_host, self.new_port))
		print ("Starting up on %s port %s" % self.new_socket.getsockname())
		self.new_socket.listen(1)
		while True:
			print ("Waiting for connection.")
			connection, client_address = self.new_socket.accept()
		self.sock.close()

	# -----------------------------------------------------------------
	def createWidgets(self):
	# -----------------------------------------------------------------
		''' Widgets are the menubar, profile, online list, toolbar. This
		function makes them. '''
		self.makeMenuBar() # Go to function to make menu bar
		self.makeProfilePage() # Go to function to show your profile
		self.makeOnlineList() # Go to function to show online contacts
		self.makeToolBar() # Go to function to make tool bar

	# -----------------------------------------------------------------
	def makeToolBar(self):
	# -----------------------------------------------------------------
		''' A tool bar at the bottom of the main window, this is below
		the show online contactslist, this toolbar includes an 'Add Contact'
		button and a 'Quit' button. '''	
		toolbar = Frame(self.master, relief=FLAT, bd=2) # Create a toolbar
		toolbar.pack(side=BOTTOM, fill=X) # Actually make it show up
		Button(toolbar, relief=GROOVE, text="Quit", command=self.quit).pack(side=RIGHT) # Button to quit the app
		Button(toolbar, relief=GROOVE, text="Add Contact", command=self.notdone).pack(side=LEFT) # Add a contact

	# -----------------------------------------------------------------
	def makeOnlineList(self):
	# -----------------------------------------------------------------
		''' Display the contacts which are online (or not(?)) and be able
		to chat with these people if you click on them. '''	
		filename = ("contacts.txt") # The name of the file to read for contacts
		self.L2 = Listbox() # Make a list to display the contacts
		try: # Try opening the file...
			f = (open(filename, "r")) # ...and read it, set it as f
			with open(filename) as my_file: # Is the file empty or not?
				my_file.seek(0) # Start looking
				first_char = my_file.read(1) # Read on the next line
				if not first_char: # If there's nothing in the file...
					self.L2.insert(END, "Your contacts list is empty, add a contact!") # ...display this
				else: # Else there's something in it
					for line in f: # For each line there is in the file...
						self.L2.insert(END, line) # ...write it in the file
			f.close() # ALWAYS CLOSE THE FILE IF YOU'VE OPENED IT!
		except: # If there is no file...
			self.L2.insert(END, "No contacts file found! Please tell an administrator.") # ...display this
		finally: # And if everything is done...
			self.L2.pack(fill=BOTH, anchor=N, expand=YES) # ...actually make it display using pack()

	# -----------------------------------------------------------------
	def makeProfilePage(self):
	# -----------------------------------------------------------------
		''' Display some of your information from the profile file, this
		is your information like name, picture(?) and whatever. '''	
		filename = ("profile.txt") # The name of the file to read for your profile
		try: # Try opening the file...
			f = (open(filename, "r")) # ...and read it, set it as f
			with open(filename) as my_file: # This whole thing
				my_file.seek(0) # Start looking
				first_char = my_file.read(1) # Read on the next line
				if not first_char: # If there's nothing in the file...
					text = ("No profile information found!") # ...display this
				else: # Else there's something in it
					for line in f:
						profile_name = line.split(",")[0]
					text = ("Welcome, " + profile_name + "!") # Display a welcome message
				f.close() # ALWAYS CLOSE THE FILE IF YOU'VE OPENED IT!
		except: # If there is no file... 
			text = ("Unable to find your profile!") # ...display this
		finally: # And if everything is done...
			L = Label(self, text=text) # Make a label to display your profile
			L.config(relief=FLAT) # Configuration of the label
			L.pack() # Displays the label

	# -----------------------------------------------------------------
	def makeMenuBar(self):
	# -----------------------------------------------------------------
		''' The menu bar, shows top of the window.
		- File: 	New chat, 
					Exit
		- Profile: 	Configurate profile
		- Contacts: Add contact, 
					Edit contact, 
					Remove contact
		- Help: 	Readme, 
					About
					Help '''
		self.MenuBar = Menu(self.master) # Name of bar, what it is(where)
		self.master.config(menu=self.MenuBar) # Configuration settings
		self.fileMenuBar() # Add file menu bar
		self.profileMenuBar() # Add profile menu bar
		self.contactsMenuBar() # Add contacts menu bar
		self.helpMenuBar() # Add help menu bar

	# -----------------------------------------------------------------
	def fileMenuBar(self):
	# -----------------------------------------------------------------
		''' Makes the File menu bar '''
		pulldown = Menu(self.MenuBar) # Creates pulldown type in the MenuBar
		# New label for the pulldown menu where if you click on it it goes to said function
		pulldown.add_command(label="New Chat", command=self.change)  # You want to start a new chat
		pulldown.add_separator() # Seperator, a small line in the pulldown menu
		pulldown.add_command(label="Exit", command=self.quit)
		self.MenuBar.add_cascade(label="File", underline=0, menu=pulldown) # Adds it to the menubar

	# -----------------------------------------------------------------
	def profileMenuBar(self):
	# -----------------------------------------------------------------
		''' Makes the Profile menu bar '''
		pulldown = Menu(self.MenuBar) # Creates pulldown type in the MenuBar
		# New label for the pulldown menu where if you click on it it goes to said function
		pulldown.add_command(label="Configurate Profile", command=self.notdone)
		self.MenuBar.add_cascade(label="Profile", underline=0, menu=pulldown) # Adds it to the menubar

	# -----------------------------------------------------------------
	def contactsMenuBar(self):
	# -----------------------------------------------------------------
		''' Makes the Contacts menu bar '''
		pulldown = Menu(self.MenuBar) # Creates pulldown type in the MenuBar
		# New label for the pulldown menu where if you click on it it goes to said function
		pulldown.add_command(label="Add a contact", command=self.notdone)
		pulldown.add_command(label="Edit a contact", command=self.notdone)
		pulldown.add_command(label="Remove a contact", command=self.notdone)
		self.MenuBar.add_cascade(label="Contacts", underline=0, menu=pulldown) # Adds it to the menubar

	# -----------------------------------------------------------------
	def helpMenuBar(self):
	# -----------------------------------------------------------------
		''' Makes the Help menu bar '''
		pulldown = Menu(self.MenuBar) # Creates pulldown type in the MenuBar
		# New label for the pulldown menu where if you click on it it goes to said function
		pulldown.add_command(label="Readme", command=self.notdone)
		pulldown.add_separator() # Seperator, a small line in the pulldown menu
		pulldown.add_command(label="About", command=self.notdone)
		pulldown.add_command(label="Help", command=self.notdone)
		self.MenuBar.add_cascade(label="Help", underline=0, menu=pulldown) # Adds it to the menubar

	# -----------------------------------------------------------------
	def notdone(self):
	# -----------------------------------------------------------------
		''' If the function has not been added yet, this shows up... '''
		tkinter.messagebox.showerror("Not implemented", "Not yet available")

	# -----------------------------------------------------------------
	def quit(self):
	# -----------------------------------------------------------------
		''' When you want to quit you get a verification first '''
		if (tkinter.messagebox.askyesno("Verify Quit", "Are you sure you want to quit?")):	
			self.sock.close()
			Frame.quit(self) # quit the frame
			# DESTROY ALL LISTENING SOCKETS BEFORE QUITTING PLEASE!

	# -----------------------------------------------------------------
	def change(self):
	# -----------------------------------------------------------------
		''' Start a new chat, first you'll have to enable it to true, then
		get an input popup to whom you want to connect, in this case it's a 
		direct connection, so it's IP+Port, you'll use your socket to retrieve
		the users name, you will also send your own information to this
		connection. '''
		start_new_chat = True # So yes, let's start a new chat
		NewChat(start_new_chat) # Go to the function for new chat

# ---------------------------------------------------------------------
class NewChat(object):
# ---------------------------------------------------------------------
	''' Opening a chat with a contact person. '''

	# -----------------------------------------------------------------
	def __init__(self, start_new_chat):
	# -----------------------------------------------------------------
		''' The constructor of the class, prepares the class for use.
		If start new chat is set to true, begin a new chat. '''
		if(start_new_chat): # Check's if its true
			self.newchatInputwindow() # If true do this

	# -----------------------------------------------------------------
	def newchatInputwindow(self):
	# -----------------------------------------------------------------
		''' When button is pressed get input from user. Make a new window
		first with labels and entry input, and if IP+Port has been inserted,
		try to connect to it and get his/her profile name, send in your own
		profile name and IP+Port he can send confirmation back to.'''
		self.connectWindow = Tk() # Creates the window
		self.connectWindow.title("Connect to?") # Title of window
		#self.connectWindow.geometry("200x40+200+200") # Size of window
		self.createWidgets() # Make the widgets in the window

	# -----------------------------------------------------------------
	def createWidgets(self):
	# -----------------------------------------------------------------
		''' Widgets in this window are labels, entry and buttons for input.
		This function makes them. '''
		Label(self.connectWindow, text="Host: ").grid(row=0, padx=1) # Label for Host
		Label(self.connectWindow, text="Port: ").grid(row=1, padx=1) # Label for Port
		
		set_input_string = StringVar() # Sets variable as a string
		set_input_int = IntVar() # Sets variable to integer
		self.input_host = Entry(self.connectWindow, textvariable=set_input_string)
		self.input_host.insert(0, "LaptopFrans")
		self.input_port = Entry(self.connectWindow, textvariable=set_input_int)
		self.input_port.insert(0, "10000")
		self.input_host.grid(row=0, column=1) # Input entry for Host
		self.input_port.grid(row=1, column=1) # Input entry for Port
		#self.input_host.focus_set() # Ik weet het niet
		#self.input_port.focus_set() # Ik weet het niet
		Button(self.connectWindow, text="Connect!", command=self.startConnecting).grid(row=3, column=0, sticky=W, padx=1) # Connect button
		Button(self.connectWindow, text="Cancel", command=self.quit).grid(row=3, column=2, sticky=W, padx=1) # Cancel button
		
	# -----------------------------------------------------------------
	def startConnecting(self):
	# -----------------------------------------------------------------
		''' Get the input information and then try to connect to said
		input and ask for name and send your stuff to him as well. '''
		#tkinter.messagebox.showerror("Not implemented", "Not yet available")
		connect_to_host = self.input_host.get() # Sets the host
		connect_to_port = int(self.input_port.get()) # Sets the port
		#print("Connecting to: " + connect_to_host + ", "+ str(connect_to_port) + "...")

		self.connect_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect_to_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.connect_to_server.connect((connect_to_host, connect_to_port))
		self.validateConnection()
		
	# -----------------------------------------------------------------
	def validateConnection(self):
	# -----------------------------------------------------------------
		''' Send your information to socket and wait for reply. '''
		filename = ("profile.txt") # The name of the file to read for your profile
		try: # Try opening the file...
			f = (open(filename, "r")) # ...and read it, set it as f
			with open(filename) as my_file: # This whole thing
				my_file.seek(0) # Start looking
				first_char = my_file.read(1) # Read on the next line
			if not first_char: # If there's nothing in the file...
				text = ("No Profile") # ...display this
			else: # Else there's something in it
				for line in f:
					profile_name = line.split(",")[0]
					profile_ip = line.split(",")[1]
					profile_port = line.split(",")[2]
					text = "Profile:," + profile_name + ',' + profile_ip + ',' + profile_port + ','
				f.close() # ALWAYS CLOSE THE FILE IF YOU'VE OPENED IT!
		except: # If there is no file... 
			text = ("No Profile") # ...display this
		finally: # And if everything is done...

			try:
				self.connect_to_server.sendall(bytes(text, "UTF-8"))
				data = self.connect_to_server.recv(256)
				print ('Received "%s"' % data)
				#print ('Received "%s"' % data.decode("UTF-8"))
			finally:
			    #print ("Socket closed.")
			    self.connect_to_server.close()

			self.connect_to_server.close()
			# Now go to check if IP and Port are valid

	# -----------------------------------------------------------------
	def quit(self):
	# -----------------------------------------------------------------
		''' No confirmation this time! '''
		self.connectWindow.destroy() # Cancels connecting
		# DESTROY ALL LISTENING SOCKETS BEFORE QUITTING PLEASE!

if (__name__ == "__main__"):
	MainSystem()