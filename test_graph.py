# coding=utf-8
from graph_tool.all import *
from random import *

import LoadData
import math
import shapefile

class CEnvironmentGraph():
    """This class instantiate a graph-tool.Graph object and set the vertex and edge properties accordingly
    to the configuration file."""

    def __init__(self, species, connections):

        self.g = Graph()  # Create new graph object
        self.species = species
        self.connections = connections
        self.num_vertex = 500

        self.names = []
        self.g.vertex_properties["position"] = self.g.new_vertex_property("vector<double>")
        self.g.vertex_properties.species = self.g.new_vertex_property("string")
        # self.gen_graph()

    def update_dimensions(self, ww, wh):
        # Update the widget dimensions where the graph is being drawn
        self.w_width = ww
        self.w_height = wh
        print("Updated dimensions", ww, wh)

    def read_shapes(self, sf):
        self.sf = shapefile.Reader(sf)
        self.x1 = self.sf.bbox[0]
        self.y1 = self.sf.bbox[1]
        self.x2 = self.sf.bbox[2]
        self.y2 = self.sf.bbox[3]
        shapes = self.sf.shapes()
        records = self.sf.records()
        print("Shapefile Max e Min values:", self.x1, self.x2, self.y1, self.y2)

    def gen_graph(self):
        self.add_vertices()
        self.calc_pos()
        self.add_edges()

    def add_vertices(self):
        # Create graph vertices and species properties for each vertex.
        self.g.add_vertex(self.num_vertex)
        vprop_name = self.g.new_vertex_property("string")
        vprop_spread_model = self.g.new_vertex_property("vector<string>")
        vprop_group = self.g.new_vertex_property("vector<string>")
        vprop_habitat = self.g.new_vertex_property("vector<string>")

        for count in range(0, self.num_vertex, 1):
            n = randint(0, len(self.species) - 1)
            s = self.species[n]

            vprop_name[count] = s["species"]
            vprop_spread_model[count] = s["spread_model"]
            vprop_group[count] = s["group"]
            vprop_habitat[count] = s["habitat"]

        self.g.vertex_properties.species = vprop_name
        self.g.vertex_properties.spread_model = vprop_spread_model
        self.g.vertex_properties.group = vprop_group
        self.g.vertex_properties.habitat = vprop_habitat

    def calc_pos(self):
        """ Set the vertices positions and return the graph object"""

        v_pos = self.g.new_vertex_property("vector<double>")
        for i in range(0, self.num_vertex, 1):
            x = randint(0, 500)
            y = randint(0, 400)
            v_pos[self.g.vertex(i)] = [x, y]
        self.g.vertex_properties["position"] = v_pos

    def add_edges(self):
        # Create edges between graph vertices, respecting the species connections and the maximum distance
        # between vertices.
        count = 0
        dist_max = 30  # Maximum acceptable distance between two vertices to create an edge.
        for s in self.connections:
            vertex_list = []
            pos_list = []
            # Create a vertex list identifying the vertex that can be connected to a specific specie, respecting the
            # relations described in connections.json.
            for v in self.g.get_vertices():
                if self.g.vertex_properties.species[v] == s:
                    vertex_list.append(v)
                    pos_list.append(self.g.vertex_properties.position[v])

            for v2 in self.g.get_vertices():
                # Create edges between vertices identified in the last step, whereas the maximum distance (in pixels)
                # between them can't be greater then the value of dist_max
                if v2 not in vertex_list and \
                        self.g.vertex_properties.species[v2] in self.connections[s]:
                    for v1 in vertex_list:
                        x1, y1 = self.g.vertex_properties.position[v1]
                        x2, y2 = self.g.vertex_properties.position[v2]
                        if math.fabs(x1 - x2) < dist_max and math.fabs(y1 - y2) < dist_max:
                            self.g.add_edge(v1, v2)
                            count += 1

            print("Count: ", count)
            count = 0

    def get_graph(self):
        return self.g
