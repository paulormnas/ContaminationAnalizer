# coding=utf-8
from graph_tool.all import *
from numpy.random import *
import numpy

_colors_defaults = {
	"S": (186 / 255, 172 / 255, 18 / 255, 0.8),
	"I": (196 / 255, 23 / 255, 23 / 255, 0.8),
	"R": (47 / 255, 174 / 255, 8 / 255, 0.8)
}


class CSIR:
	def __init__(self):
		# SIRS dynamics parameters:
		self.x = 0.001  # spontaneous outbreak probability
		self.r = 0.1  # I->R probability
		self.s = 0.01  # R->S probability
		self.sinks = []

	def random_infect(self, g):
		"""
		Choose a random vertex to change it's state to infected and update it's properties
		:param g: The graph used o simulation
		:type g: graph_tool.Graph
		:return: None
		:rtype: None
		"""
		trials = 0
		while trials < g.num_vertices():
			v_index = randint(0, g.num_vertices() - 1)
			v = g.vertex(v_index)
			if g.vertex_properties.state[v][0] is "I":
				trials += 1
			else:
				g.vertex_properties.state_color[v] = _colors_defaults["I"]
				g.vertex_properties.state[v][0] = "I"
				break

	def infect(self, graph, index, neighbors_list, source, is_forward, vertex_states, iteration):
		for n in neighbors_list:
			# Verify if neighbor can be infected by same type of Tc being spread from source vertex
			group = graph.vertex_properties.group[source][index]  # Identify the type of Tc
			if group in graph.vertex_properties.group[n]:
				group_list = list(graph.vertex_properties.group[n])
				n_index = group_list.index(group)
				if is_forward:
					if graph.vertex_properties.spread_model[n][n_index] == "SI":
						#  TODO: fix step backward infection
						# Infect neighbor using SI model
						self.si(graph=graph,
						        v=n,
						        index=n_index)

						#  TODO: Implement others spread models
					# if graph.vertex_properties.spread_model[n][nindex] is "SIS":
					# 	self.sm.sis()  # Infect neighbor using SIS model
					# if graph.vertex_properties.spread_model[n][nindex] is "SIR":
					# 	self.sm.sir()  # Infect neighbor using SIR model
				else:
					states = vertex_states[iteration]
					state = states[graph.vertex_index[n]]
					print("State_Before:", graph.vertex_properties.state[n][n_index])
					graph.vertex_properties.state[n][n_index] = state[n_index]
					print("State read from dict:", state[n_index])
					print("State_After:", graph.vertex_properties.state[n][n_index])
					color = _colors_defaults[state[n_index]]
					graph.vertex_properties.state_color[n] = color

	def si(self, graph, v, index):
		graph.vertex_properties.state[v][index] = "I"
		graph.vertex_properties.state_color[v] = _colors_defaults["I"]
