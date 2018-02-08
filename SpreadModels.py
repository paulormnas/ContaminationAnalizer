# coding=utf-8
from graph_tool.all import *
from random import *

_colors_defaults = {
	"S": (47 / 255, 174 / 255, 8 / 255, 0.8),
	"I": (196 / 255, 23 / 255, 23 / 255, 0.8),
	"R": (186 / 255, 172 / 255, 18 / 255, 0.8)
}


class CSIR:
	def __init__(self, graph):
		self.graph = graph
		# SIRS dynamics parameters:
		self.x = 0.001  # spontaneous outbreak probability
		self.r = 0.1  # I->R probability
		self.s = 0.01  # R->S probability

	def random_infect(self):
		"""
		Choose a random vertex to change it's state to infected and update it's properties
		:return: None
		:rtype: None
		"""
		v_index = randint(0, self.graph.num_vertices() - 1)
		v = self.graph.vertex(v_index)
		self.graph.vertex_properties.state_color[v] = _colors_defaults["I"]
		self.graph.vertex_properties.state[v][0] = "I"

