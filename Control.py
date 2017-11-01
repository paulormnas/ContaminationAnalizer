# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from graph_tool.all import *

import test_graph

class CController():
# This class is used to conect que View class to the others. It is a intermediate class responsible for manage
# the information transit between classes

	def __init__(self):
		self.graph = test_graph.CEnvironmentGraph()
		pass

	def on_button_clicked(self, widget):
		print("Hello World!")

	def print_debug(self, widget):
		print(dir(Gtk.Box.props))

	def get_graph(self):
		return self.graph.get_graph()