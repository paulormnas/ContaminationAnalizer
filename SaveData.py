# coding=utf-8
import json


class CSaveData:
	def __init__(self):
		pass

	def save_species(self, data):
		"""Save species properties to the file in JSON format"""
		with open("config/species.json", "w") as data_file:
			json.dump(data, data_file, indent=2)

	def save_connections(self, data):
		"""Save species connections specifications to the file in JSON format"""
		with open("config/connections.json", "w") as data_file:
			json.dump(data, data_file, indent=2)