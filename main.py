from graph_tool.all import *

g = Graph()
v1 = g.add_vertex()
v2 = g.add_vertex()
vprop_name = g.new_vertex_property("string")
vprop_name[v1] = "Coati"
vprop_name[v2] = "Ocelot"
e = g.add_edge(v1,v2)

graph_draw(g, vertex_text=g.vertex_index, vertex_font_size=18,
           output_size=(200, 200), output="two-nodes.png")

g.save("inicial_graph.gt")

from itertools import izip
from numpy.random import randint

g2 = Graph()
g2.add_vertex(100)
# insert some random links
for s,t in izip(randint(0, 100, 100), randint(0, 100, 100)):
    g2.add_edge(g2.vertex(s), g2.vertex(t))

graph_draw(g2, vertex_text=g2.vertex_index, vertex_font_size=18,
           output_size=(1200, 1200), output="100-nodes.png")