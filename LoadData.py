# coding=utf-8
import json


class CLoadData:
	def __init__(self):
		pass

	def read_spread_models(self):
		"""Read the spread models specified in the JSON file"""
		with open("config/spread_models.json", "r") as data_file:
			data = json.loads(data_file.read())
		return data["spread_models"]

	def read_habitats(self):
		"""Read the habitats specified in the JSON file"""
		with open("config/habitats.json", "r") as data_file:
			data = json.loads(data_file.read())
		return data["habitats"]

	def read_species(self):
		"""Read the species specified in the JSON file and they properties"""
		with open("config/species.json", "r") as data_file:
			data = json.loads(data_file.read())
		return data

	def read_connections(self):
		"""Read the connections specified in the JSON file for each species"""
		with open("config/connections.json", "r") as data_file:
			data = json.loads(data_file.read())
		return data
