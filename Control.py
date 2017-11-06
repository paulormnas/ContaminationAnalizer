# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from graph_tool.all import *

import test_graph
import SER

class CController():
# This class is used to conect que View class to the others. It is a intermediate class responsible for manage
# the information transit between classes

	def __init__(self):
		self.env_graph = test_graph.CEnvironmentGraph()
		self.graph = self.env_graph.get_graph()
		self.ser = SER.CSER()

	def on_button_clicked(self, widget):
		print("Hello World!")

	def print_debug(self, widget):
		print(dir(Gtk.Box.props))

	def get_graph(self):
		return self.env_graph.get_graph()

	def step_forward(self, graph):
		return self.ser.run(g=graph)