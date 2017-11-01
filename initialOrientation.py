# coding=utf-8
from graph_tool.all import *

def revertEdge(graph, edge):
	edge2 = graph.add_edge(edge.target(), edge.source())
	# print(edge.source(), edge.target())
	# print(edge2.source(), edge2.target())
	eprop_criterio = graph.edge_properties["criterioContaminacao"]
	eprop_criterio[(edge2.source(), edge2.target())] = eprop_criterio[(edge.source(), edge.target())]
	graph.edge_properties["criterioContaminacao"] = eprop_criterio
	graph.remove_edge(edge)

def concurrencyMeasure(graph):
	concurrency = 0
	for v in graph.vertices():
		if (v.in_degree() > 0) and (v.out_degree() == 0):
			print("Vertex index ", graph.vertex_index[v])
			concurrency = concurrency + 1
	return concurrency

g = Graph()
g.load("inicial_graph.gt")
print("Concurrency", concurrencyMeasure(g))
revertEdge(g, g.edge(0, 1))
print("Concurrency", concurrencyMeasure(g))
# g.set_directed(False)

# graph_tool.draw.interactive_window(g, vertex_size=80, vertex_text=g.vertex_properties["name"], vertex_text_position=-5,
#                                    vertex_font_size=12, edge_pen_width=g.edge_properties["criterioContaminacao"],
#                                    geometry=(1440, 1024), edge_marker_size=30)



# graph_tool.draw.interactive_window(g, vertex_size=80, vertex_text=g.vertex_properties["name"], vertex_text_position=-5,
#                                    vertex_font_size=12, edge_pen_width=g.edge_properties["criterioContaminacao"],
#                                    geometry=(1440, 1024), edge_marker_size=30)