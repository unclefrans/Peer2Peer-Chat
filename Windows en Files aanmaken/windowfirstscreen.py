from tkinter import *
import tkinter.messagebox
import os
import threading
import time
import socket
import select
import sys

class MainScreen(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack()
		self.createWidgets()
		self.master.title("Peer2Peer Chat")
		self.master.iconname("tkpython")
		self.master.geometry("400x350+200+200")
		threading.Thread(target=self.opensocket).start()

	def readOwnProfile(self):
		filename = ("profile.txt")
		try:
			f = (open(filename, "r"))
			with open(filename) as my_file:
				my_file.seek(0)
				first_char = my_file.read(1)
				if not first_char:
					text = ("No profile information found!")
				else:
					text = ("Welcome, " + f.read() + "!")
				f.close()
		except:
			text = ("Unable to find your profile!")
		finally:
			L = Label(self, text=text)
			L.config(relief=FLAT)
			L.pack()

	def readContactList(self):
		filename = ("contacts.txt")
		self.L2 = Listbox()
		try:
			f = (open(filename, "r"))
			with open(filename) as my_file:
				my_file.seek(0)
				first_char = my_file.read(1)
				if not first_char:
					self.L2.insert(END, "Your contacts list is empty, add a contact!")
				else:
					for line in f:
						self.L2.insert(END, line)
			f.close()
		except:
			self.L2.insert(END, "No contacts file found! Please tell an administrator.")
		finally:
			self.L2.pack(fill=BOTH, anchor=N, expand=YES)
			

	def createWidgets(self):
		self.makeMenuBar()
		self.makeToolBar()
		self.readOwnProfile()
		self.readContactList()	

	def makeToolBar(self):
		toolbar = Frame(self.master, relief=FLAT, bd=2)
		toolbar.pack(side=BOTTOM, fill=X)
		Button(toolbar, relief=GROOVE, text="Quit", command=self.quit).pack(side=RIGHT)
		Button(toolbar, relief=GROOVE, text="Add Contact", command=AddContactScreen).pack(side=LEFT)

	def makeMenuBar(self):
		self.menubar = Menu(self.master)
		self.master.config(menu=self.menubar)
		self.fileMenu()
		self.profileMenu()
		self.contactsMenu()
		self.helpMenu()

	def fileMenu(self):
		pulldown = Menu(self.menubar)
		pulldown.add_command(label="New Chat", command=self.openNewChat)
		pulldown.add_separator()
		pulldown.add_command(label="Exit", command=self.quit)
		self.menubar.add_cascade(label="File", underline=0, menu=pulldown)

	def profileMenu(self):
		pulldown = Menu(self.menubar)
		pulldown.add_command(label="Configurate Profile", command=self.notdone)
		self.menubar.add_cascade(label="Profile", underline=0, menu=pulldown)

	def contactsMenu(self):
		pulldown = Menu(self.menubar)
		pulldown.add_command(label="Add a contact", command=AddContactScreen)
		pulldown.add_command(label="Edit a contact", command=self.notdone)
		pulldown.add_command(label="Remove a contact", command=self.notdone)
		self.menubar.add_cascade(label="Contacts", underline=0, menu=pulldown)

	def helpMenu(self):
		pulldown = Menu(self.menubar)
		pulldown.add_command(label="Readme", command=self.notdone)
		pulldown.add_separator()
		pulldown.add_command(label="About", command=self.notdone)
		self.menubar.add_cascade(label="Help", underline=0, menu=pulldown)

	def greeting(self):
		tkinter.messagebox.showinfo("greeting", "Greetings")

	def notdone(self):
		tkinter.messagebox.showerror("Not implemented", "Not yet available")

	def quit(self):
		if (tkinter.messagebox.askyesno("Verify Quit", "Are you sure you want to quit?")):	
			self.closeownsocket()
			Frame.quit(self)

	def openNewChat(self):
		self.chatwindow = Tk()
		self.chatwindow.title("Start new chat")
		self.newchatInput()

	def newchatInput(self):
		var = StringVar()
		var.set(self.chatwindow.title())
		self.entry = Entry(self.chatwindow, textvariable=var)
		self.entry.focus_set()
		self.entry.pack(padx=5, side=LEFT, anchor=NW)
		Button(self.chatwindow, relief=GROOVE, text="Connect!", command=self.beginchat).pack(side=LEFT, anchor=NW)

	def beginchat(self):
		#self.chatwindow.title(self.entry.get())
		entry_input = self.entry.get()
		self.connecttoaddr(entry_input)

	def opensocket(self):
		my_server_host = socket.gethostname()
		my_server_port = 8888
		self.my_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.my_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.my_server.bind((my_server_host, my_server_port))
		self.my_server.listen(5)
		while True:
			client, client_address = self.my_server.accept()
			print("Connection from", client_address)
		self.my_server.close()

	def closeownsocket(self):
		self.my_server.close()

	def connecttoaddr(self, entry_input):
		connect_to_host = socket.gethostname()
		connect_to_port = int(entry_input)
		connect_to_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		connect_to_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		connect_to_server.connect((connect_to_host, connect_to_port))
		connect_to_server.close()

class AddContactScreen(object):
	def __init__(self):
		self.addcontactWindow = Tk()
		self.addcontactWindow.title("Add Contact")
		self.addcontactWindowInput()

	def addcontactWindowInput(self):
		var = StringVar()
		var.set(self.addcontactWindow.title())
		self.entry = Entry(self.addcontactWindow, textvariable=var)
		self.entry.focus_set()
		self.entry.pack(padx=5, side=LEFT, anchor=NW)
		Button(self.addcontactWindow, relief=GROOVE, text="Confirm", command=self.addtoProfileList).pack(side=LEFT, anchor=NW)

	def addtoProfileList(self):
		insert_contact = self.entry.get() # NEED TO ENCODE THIS FOR SECURITY!
		filename = ("contacts.txt")

		# Insert input to contact list
		f = (open(filename, "a"))
		f.write(insert_contact + "\n")
		f.close()

		f = (open(filename, "r"))
		with open(filename) as my_file: # Check if empty file
			my_file.seek(0)
			first_char = my_file.read(1)
			L2.delete(0, tkinter.END) # Clear
			if not first_char:
				L2.insert(END, "Your contacts list is empty, add a contact!")
			else:
				for line in f: # If not empty write contacts list
					L2.insert(END, line) 
		f.close()
		self.addcontactWindow.destroy()

if (__name__ == "__main__"):
	MainScreen().mainloop()