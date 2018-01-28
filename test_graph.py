# coding=utf-8
from graph_tool.all import *
from random import *

import LoadData
import math

class CEnvironmentGraph():
    """This class instantiate a graph-tool.Graph object and set the vertex and edge properties accordingly
    to the configuration file."""

    def __init__(self, species, connections):

        self.g = Graph()  # Create new graph object
        self.species = species
        self.connections = connections
        self.num_vertex = 200

        self.names = []
        self.contaminationCriteria = []
        self.count = 0
        self.g.vertex_properties["position"] = self.g.new_vertex_property("vector<double>")

        self.read_data()
        self.add_vertex()
        self.calc_pos()
        self.add_edge()

    def read_data(self):
        """ Read data from "dados_animais.txt" to set the graph properties"""
        # ocorrencia = []
        # dataFile = open("dados_animais.txt", "r", encoding='utf-8')
        #
        # for line in dataFile:
        #     if self.count != 0:
        #         self.names.append(line[:line.index('\t')])
        #         line = line[line.index('\t') + 1:]
        #         self.contaminationCriteria.append(line[:line.index('\t')])
        #         line = line[line.index('\t') + 1:]
        #         if line[len(line) - 1] == '\n':
        #             ocorrencia.append(line[:len(line) - 1])
        #         else:
        #             ocorrencia.append(line)
        #     self.count = self.count + 1



    def add_vertex(self):
        """ Add vertex to the graph with the properties read from the file"""
        # self.g.add_vertex(self.count - 1)
        #
        # vprop_name = self.g.new_vertex_property("string")  # Add properties to the vertex
        #
        # self.count = 0
        # for name in self.names:  # Name the vertex
        #     vprop_name[self.count] = name
        #     self.count = self.count + 1
        #
        # self.g.vertex_properties["name"] = vprop_name  # Internalize de property "name"
        #
        # vprop_criterion = self.g.new_vertex_property("double")  # Add property to the vertices
        #
        # self.count = 0
        # for value in self.contaminationCriteria:  # Define contamination criterion of vertices
        #     vprop_criterion[self.count] = float(value)
        #     self.count = self.count + 1
        #
        # self.g.vertex_properties[
        #     "contaminationCriteria"] = vprop_criterion  # Internalize the property "contaminationCriteria"

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

    def add_edge(self):
        """ Create edges between vertices"""
        # vprop_criterion = self.g.vertex_properties["contaminationCriteria"]
        # eprop_criterion = self.g.new_edge_property("double")  # Add property to the edges
        #
        # for i in range(1, 8):
        #     self.g.add_edge(0, i)
        #     eprop_criterion[(0, i)] = vprop_criterion.a[0] / 10
        #
        # for i in range(1, 4):
        #     self.g.add_edge(6, i)
        #     eprop_criterion[(6, i)] = vprop_criterion.a[i] / 10
        #     self.g.add_edge(7, i)
        #     eprop_criterion[(7, i)] = vprop_criterion.a[i] / 10
        #
        # self.g.edge_properties["contaminationCriteria"] = eprop_criterion
        count = 0
        dist_max = 50  # Max distance to put a edge between two vertices
        for s in self.connections:
            vertex_list = []
            pos_list = []
            for v in self.g.get_vertices():
                if self.g.vertex_properties.species[v] == s:
                    vertex_list.append(v)
                    pos_list.append(self.g.vertex_properties.position[v])

            for v2 in self.g.get_vertices():

                if v2 not in vertex_list and \
                        self.g.vertex_properties.species[v2] in self.connections[s]:
                    for v1 in vertex_list:
                        x1, y1 = self.g.vertex_properties.position[v1]
                        x2, y2 = self.g.vertex_properties.position[v2]
                        if(math.fabs(x1 - x2) < dist_max and math.fabs(y1 - y2) < dist_max):
                            self.g.add_edge(v1, v2)
                            count += 1

            print("Count: ", count)
            count = 0

    def get_graph(self):
        return self.g
