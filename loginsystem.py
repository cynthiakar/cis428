import json
from security import check_encrypted_password
import os

class LoginSystem:
	def __init__(self):
		self.usersDB = {}
		with open('usersDB.json') as f:
			self.usersDB = json.load(f)
		print(self.usersDB)

	def createAccount(self, username, password):
		if username in list(self.usersDB.keys()):
			return False
		self.usersDB[username] = password
		with open('usersDB.json', 'w') as f:
				json.dump(self.usersDB, f)
		return True

	def login(self, username, password):
		return check_encrypted_password(password, self.usersDB[username])

