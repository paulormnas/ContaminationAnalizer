# coding=utf-8
import json


class CLoadData:
    def __init__(self):
        pass

    @staticmethod
    def read_spread_models():
        """Read the spread models specified in the JSON file"""
        with open("config/spread_models.json", "r") as data_file:
            data = json.loads(data_file.read())
        return data["spread_models"]

    @staticmethod
    def read_habitats():
        """Read the habitats specified in the JSON file"""
        with open("config/habitats.json", "r") as data_file:
            data = json.loads(data_file.read())
        return data["habitats"]

    @staticmethod
    def read_species():
        """Read the species specified in the JSON file and they properties"""
        with open("config/species.json", "r") as data_file:
            data = json.loads(data_file.read())
        return data

    @staticmethod
    def read_connections():
        """Read the connections specified in the JSON file for each species"""
        with open("config/connections.json", "r") as data_file:
            data = json.loads(data_file.read())
        return data
