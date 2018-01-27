# coding=utf-8
from graph_tool.all import *

class CSER:
	"""This class is responsible for implement the Scheduling by Edge Reversal algorithm and control the simulation."""
	def __init__(self):
		self.sinks = []
		self.iterations = 0

	def get_iterations_number(self):
		return self.iterations

	def run(self, g, is_forward):
		"""Verify if is a forward or backward step and revert the edges accordingly to each movement"""
		if is_forward:
			self.concurrency_measure(g)
			self.iterations += 1
		elif self.iterations > 0:
			self.identify_last_sinks(g)
			self.iterations -= 1

		self.revert_edge(g, is_forward=is_forward)
		return g

	def reset(self, g):
		"""Runs the SER algorithm backwards until it reaches the initial state"""
		while self.iterations:
			g = self.run(g=g, is_forward=False)
		return g

	def concurrency_measure(self, graph):
		"""Identify the vertices that are sink in this moment and create a list with they indexes."""
		concurrency = 0
		for v in graph.vertices():
			if (v.in_degree() > 0) and (v.out_degree() == 0):
				self.sinks.append(graph.vertex_index[v])
				concurrency += 1

	def identify_last_sinks(self, graph):
		"""Identify the vertices that operated in the last iteration and create a list with they indexes."""
		last_sink = 0
		for v in graph.vertices():
			if (v.out_degree() > 0) and (v.in_degree() == 0):
				self.sinks.append(graph.vertex_index[v])
				last_sink += 1

	def revert_edge(self, graph, is_forward):
		"""Revert all edges of all vertices in self.sinks list, regarding as a step forward or backward"""
		for sink in self.sinks:
			if is_forward:
				neighbors_list = graph.get_in_neighbors(sink)
			else:
				neighbors_list = graph.get_out_neighbors(sink)

			for neighbor in neighbors_list:
				if is_forward:
					old_edge = graph.edge(neighbor, sink)
					new_edge = graph.add_edge(sink, neighbor)
				else:
					old_edge = graph.edge(sink, neighbor)
					new_edge = graph.add_edge(neighbor, sink)

				# eprop_criterio = graph.edge_properties["contaminationCriteria"]
				# eprop_criterio[(new_edge.source(), new_edge.target())] = eprop_criterio[(old_edge.source(), old_edge.target())]
				# graph.edge_properties["contaminationCriteria"] = eprop_criterio
				graph.remove_edge(old_edge)

		self.sinks = []