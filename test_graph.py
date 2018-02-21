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
        self.max_vertex = 5000
        self.v_total = 0
        self.pixel_step = 20

        self.names = []
        self.v_pos = []
        self.g.vertex_properties.position = self.g.new_vertex_property("vector<double>")
        self.g.vertex_properties.species = self.g.new_vertex_property("string")
        self.g.vertex_properties.spread_model = self.g.new_vertex_property("vector<string>")
        self.g.vertex_properties.group = self.g.new_vertex_property("vector<string>")
        self.g.vertex_properties.habitat = self.g.new_vertex_property("vector<string>")
        self.g.vertex_properties.state = self.g.new_vertex_property("vector<string>")
        self.g.vertex_properties.state_color = self.g.new_vertex_property("vector<double>")

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
        self.shapes = self.sf.shapes()
        records = self.sf.records()

    def gen_graph(self):
        self.calc_pos()
        self.add_vertices()
        self.add_edges()

    def calc_pos(self):
        """ Set the vertices positions"""
        width_ratio = float(self.w_width) / float(self.w_width / 4)
        height_ratio = float(self.w_height) / float(self.w_height / 3)
        scale_xy = min(width_ratio, height_ratio)

        v_count = 0
        for i in range(len(self.shapes)):
        # for i in range(0, 10):
            if v_count < self.max_vertex:
                coords = self.shapes[i].points
                x_max, x_min, y_max, y_min = coords[0][0], coords[0][0], coords[0][1], coords[0][1]
                # Find maximum and minimum value of shapes coordinates
                for i in range(len(coords)):
                    if coords[i][0] > x_max:
                        x_max = coords[i][0]
                    if coords[i][0] < x_min:
                        x_min = coords[i][0]

                    if coords[i][1] > y_max:
                        y_max = coords[i][1]
                    if coords[i][1] < y_min:
                        y_min = coords[i][1]
                # print(x_max, x_min, y_max, y_min)

                # Normalize maximum and minimum values of shape coordinates and convert to widget dimensions
                x_max_norm = (x_max - self.x1) / (self.x2 - self.x1)
                y_max_norm = (y_max - self.y1) / (self.y2 - self.y1)
                x_min_norm = (x_min - self.x1) / (self.x2 - self.x1)
                y_min_norm = (y_min - self.y1) / (self.y2 - self.y1)

                x_max = int((x_max_norm * self.w_width) / 4)
                x_min = int((x_min_norm * self.w_width) / 4)
                y_max = int((y_max_norm * self.w_height) / 3)
                y_min = int((y_min_norm * self.w_height) / 3)

                # Set coordinates where the vertices should be drawn
                for column in range(0, int(self.w_width / 4), self.pixel_step):
                    if v_count < self.max_vertex:
                        for row in range(0, int(self.w_height / 3), self.pixel_step):
                            # print(x_min, column, x_max, y_min, row, y_max)

                            if x_min <= column <= x_max and y_min <= row <= y_max:
                                if v_count < self.max_vertex and [column, row] not in self.v_pos:
                                    self.v_pos.append([column, row])
                                    v_count += 1
                                else:
                                    break
                    else:
                        break
            else:
                break
        print("Vertices total:", v_count)
        self.v_total = v_count - 1

    def add_vertices(self):
        """
        Create graph vertices and species properties for each vertex.
        :return: None
        :rtype: None
        """
        self.g.add_vertex(self.v_total)
        vprop_pos = self.g.new_vertex_property("vector<double>")

        # Read the species properties from the JSON file and insert into vertex properties
        for v in self.g.vertices():
            n = randint(0, len(self.species) - 1)
            s = self.species[n]
            self.g.vertex_properties.species[v] = s["species"]
            self.g.vertex_properties.spread_model[v] = s["spread_model"]
            self.g.vertex_properties.group[v] = s["group"]
            self.g.vertex_properties.habitat[v] = s["habitat"]
            self.g.vertex_properties.state[v] = s["state"]
            # Color for susceptible (S) state
            self.g.vertex_properties.state_color[v] = (186 / 255, 172 / 255, 18 / 255, 0.8)

        for count in range(0, self.v_total, 1):
            vprop_pos[count] = self.v_pos[count]

        self.g.vertex_properties.position = vprop_pos

    def add_edges(self):
        # Create edges between graph vertices, respecting the species connections and the maximum distance
        # between vertices.
        count = 0
        total = 0
        dist_max = self.pixel_step  # Maximum acceptable distance between two vertices to create an edge.
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
                if v2 not in vertex_list and self.g.vertex_properties.species[v2] in self.connections[s]:
                    for v1 in vertex_list:
                        x1, y1 = self.g.vertex_properties.position[v1]
                        x2, y2 = self.g.vertex_properties.position[v2]
                        # print(x1, y1, x2, y2)
                        # print(self.g.edge(v1, v2), self.g.edge(v2, v1))
                        if math.fabs(x1 - x2) <= dist_max and math.fabs(y1 - y2) <= dist_max and \
                            self.g.edge(v1, v2) is None and self.g.edge(v2, v1) is None:
                            self.g.add_edge(v1, v2)
                            count += 1
            total += count
            print(s, count)
            count = 0
        print("Total:", total)

    def get_graph(self):
        """Return the graph object"""
        return self.g
