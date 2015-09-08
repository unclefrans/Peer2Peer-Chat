# Imports
import os
import sys
import datetime

profile_filename = ("profile.txt")	
profile_filepath = ("Profile")

class MainClass():
	def path_Profile():
		if not os.path.exists(profile_filepath):
			os.makedirs(profile_filepath)
			profile_filename = ("profile.txt")
	def get_Profile():
		try:
			with open(os.path.join(profile_filepath, profile_filename), "r+") as temp_file:
				temp_file.seek(0)
				temp_file.read(1)
		except:
			MainClass.create_Profile()
	def create_Profile():
		with open(os.path.join(profile_filepath, profile_filename), "w+") as temp_file:
			temp_file.write("Frans,LaptopFrans,1000,")

MainClass.path_Profile()
MainClass.get_Profile()