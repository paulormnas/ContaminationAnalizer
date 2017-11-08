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
		# Instantiate the classes that will be controlled by CController
		self.env_graph = test_graph.CEnvironmentGraph()
		self.graph = self.env_graph.get_graph()
		self.ser = SER.CSER()

	def get_graph(self):
		# Get the graph that will be drawn in the environment page
		return self.env_graph.get_graph()

	def get_iterations(self):
		return self.ser.get_iterations_number()

	def step_backward(self, graph):
		# Start a backward step in SER algorithm and return the graph to be drawn
		return self.ser.run(g=graph, is_forward=False)

	def step_forward(self, graph):
		# Start a forward step in SER algorithm and return the graph to be drawn
		return self.ser.run(g=graph, is_forward=True)

	def reset(self, graph):
		# Reset the SER algorithm for the initial state and return the graph to be drawn
		return self.ser.reset(g=graph)
