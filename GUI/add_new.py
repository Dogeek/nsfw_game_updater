#-*- encoding:utf8 -*-
#!/usr/bin/python3

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import json
import os
import requests

from constants import *
from exceptions import *

def load_json():
	with open('games.json', 'r') as jsonfile:
		return json.loads(jsonfile.read())

# Check if this url was shortened
def is_shortened(url):
	return "goo.gl" in url

def unshorten_url(url):
	resp = requests.head(url, allow_redirects=True)
	return resp.url

def check_url(url):
	if is_shortened(url):
		return unshorten_url(url)
	return url

def game_exists(game_name, db=None):
	if db is None:
		with open('games.json', 'r') as jsonfile:
			db = json.loads(jsonfile.read())
	for sub_array in db:
		if sub_array["game"].lower() == game_name.lower():
			return True
	return False

def add_new_game(json_to_add):
	"""
		Adds a new game to the database, checking if a game named similarly is already present.
		If a game is already in the database, raises a DatabaseError exception
	"""
	with open('games.json', 'r') as jsonfile:
		db = json.loads(jsonfile.read())
	if game_exists(json_to_add["game"], db):
		raise DatabaseError("Game with that title and developer is already in DB")
	json_list = []

	for sub_array in db:
		json_list.append(sub_array)
	json_list.append(json_to_add)
	with open('temp_json', 'w', encoding="utf-8") as f:
		 f.write(json.dumps(json_list, indent=4, sort_keys=True))
	os.remove("games.json")
	os.rename("temp_json", "games.json")

class AddNewGUI(tk.Toplevel):
	def __init__(self, master = None):
		super(AddNewGUI, self).__init__()
		self.master = master
		self.title = "Add a new Game"
		self.animation = tk.StringVar()
		self.developer = tk.StringVar()
		self.dl_android = tk.StringVar()
		self.dl_linux = tk.StringVar()
		self.dl_windows = tk.StringVar()
		self.dl_mac = tk.StringVar()
		self.engine = tk.StringVar()
		self.game = tk.StringVar()
		self.genre = tk.StringVar()
		self.graphtreon = tk.StringVar()
		self.latest_version = tk.StringVar()
		self.public_build = tk.StringVar()
		self.setting = tk.StringVar()
		self.visual_style = tk.StringVar()
		self.config()
		pass

	def config(self):
		"""
		template :
			"animation": "Yes",
			"developer": "Insexsity_team",
			"download_link_android": "http://insexsity.com/0.265_Android_(U).apk",
			"download_link_linux": "http://insexsity.com/0.265_Linux_64_(U).zip",
			"download_link_mac": "http://insexsity.com/0.265_Mac_64_(U).zip",
			"download_link_windows": "http://insexsity.com/0.265_PC_64_(U).zip",
			"engine": "Unity",
			"game": "Insexsity",
			"genre": "Sandbox/adventure",
			"graphtreon": "https://graphtreon.com/creator/insexsity",
			"latest_version": "0.265",
			"public_build": "http://insexsity.com/download.html",
			"setting": "Contemporary",
			"visual_style": "2D anime"
		"""
		engines = ('Adrift', "Flash", "Godot", "HTML", "Java", "Other", "RPGM", "Ren'Py", "UE4", "Unity")
		settings = ('Contemporary', 'Contemporary Fantasy', 'Fantasy', 'Sci-fi', 'Sci-fi Fantasy')
		visual_styles = ('2D Furry', '2D anime', '2D comic/cartoon', '2D pixel', '2D vector', '2D western',\
		 '3D DAZ renders', '3D anime', '3D anime renders', '3D realistic', '3D stylized', 'Photos', 'Text', 'Text(UI icons)')

		ttk.Combobox(self, textvariable = self.animation, state='readonly', values=("Yes", "No")).grid(row=0, column=1)
		tk.Label(self, text="Animation :").grid(row=0, column=0)

		tk.Entry(self, textvariable=self.developer).grid(row=1, column=1)
		tk.Label(self, text="Developer :").grid(row=1, column=0)

		tk.Entry(self, textvariable=self.dl_android).grid(row=2, column=1)
		tk.Label(self, text="Link(Android) :").grid(row=2, column=0)

		tk.Entry(self, textvariable=self.dl_linux).grid(row=3, column=1)
		tk.Label(self, text="Link(Linux) :").grid(row=3, column=0)

		tk.Entry(self, textvariable=self.dl_mac).grid(row=4, column=1)
		tk.Label(self, text="Link(MacOS) :").grid(row=4, column=0)

		tk.Entry(self, textvariable=self.dl_windows).grid(row=5, column=1)
		tk.Label(self, text="Link(Windows) :").grid(row=5, column=0)

		ttk.Combobox(self, textvariable = self.engine, state='readonly', values=engines).grid(row=6, column=1)
		tk.Label(self, text="Engine :").grid(row=6, column=0)

		tk.Entry(self, textvariable=self.game).grid(row=7, column=1)
		tk.Label(self, text="Game :").grid(row=7, column=0)

		tk.Entry(self, textvariable=self.graphtreon).grid(row=8, column=1)
		tk.Label(self, text="Graphtreon :").grid(row=8, column=0)

		tk.Entry(self, textvariable=self.latest_version).grid(row=9, column=1)
		tk.Label(self, text="Latest Version :").grid(row=9, column=0)

		tk.Entry(self, textvariable=self.public_build).grid(row=10, column=1)
		tk.Label(self, text="Public Build :").grid(row=10, column=0)

		ttk.Combobox(self, textvariable = self.setting, state='readonly', values=settings).grid(row=11, column=1)
		tk.Label(self, text="Setting :").grid(row=11, column=0)

		ttk.Combobox(self, textvariable = self.visual_style, state='readonly', values=visual_styles).grid(row=12, column=1)
		tk.Label(self, text="Visual Style :").grid(row=12, column=0)


		self.ok_button = tk.Button(self, text="Ok", command=self.onOkButton)
		self.cancel_button = tk.Button(self, text="Cancel", command=self.onCancelButton)
		self.ok_button.grid(column=0, row=20)
		self.cancel_button.grid(column=1, row=20)
		self.loopCheck()
		pass

	def onFilepathButton(self):
		directory = askdirectory()
		self.filepath_var.set(directory)
		pass

	def onOkButton(self):
		json_to_add = {\
		"game": self.game.get(), \
		"public_build": self.public_build.get(),\
		"setting":self.setting.get(),\
		"developer": self.developer.get(),\
		"engine": self.engine.get(),\
		"visual_style":self.visual_style.get(),\
		"genre":self.genre.get(),\
		"animation":self.animation.get(),\
		"latest_version":self.latest_version.get(),\
		"download_link_windows": check_url(self.dl_windows.get()),\
		"download_link_mac": check_url(self.dl_mac.get()),\
		"download_link_linux": check_url(self.dl_linux.get()),\
		"download_link_android": check_url(self.dl_android.get()),\
		"graphtreon": self.graphtreon.get()}
		try:
			add_new_game(json_to_add)
		except DatabaseError as e:
			messagebox.showerror('Error', message=e)
		finally:
			self.quit()
	def onCancelButton(self):
		self.quit()

	def quit(self):
		global ADD_NEW_OPEN

		ADD_NEW_OPEN = False
		self.destroy()
		pass

	def loopCheck(self):
		self.after(20, self.loopCheck)
		pass
	pass
