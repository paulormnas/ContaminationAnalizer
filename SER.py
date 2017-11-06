# coding=utf-8
from graph_tool.all import *
import Control

class CSER:
	# This class is responsible for implement the Scheduling by Edge Reversal algorithm and control the simulation.
	def __init__(self):
		self.sinks = []

	def revertEdge(self, graph):
		# Revert all edges of all vertices that are sinks in this moment
		for sink in self.sinks:
			v = graph.vertex(sink)
			for old_edge in v.all_edges():
				new_edge = graph.add_edge(old_edge.target(), old_edge.source())
				eprop_criterio = graph.edge_properties["contaminationCriteria"]
				eprop_criterio[(new_edge.source(), new_edge.target())] = eprop_criterio[(old_edge.source(), old_edge.target())]
				graph.edge_properties["contaminationCriteria"] = eprop_criterio
				graph.remove_edge(old_edge)
		self.sinks = []

	def concurrencyMeasure(self, graph):
		# Identify the vertices that are sink in this moment and create a list with they indexes.
		concurrency = 0
		for v in graph.vertices():
			if (v.in_degree() > 0) and (v.out_degree() == 0):
				self.sinks.append(graph.vertex_index[v])
				concurrency = concurrency + 1


	def run(self, g):
		self.concurrencyMeasure(g)
		self.revertEdge(g)
		return g