# coding=utf-8
from graph_tool.all import *
from random import *

class CEnvironmentGraph():

# This class instaciate a graph-tool.Graph object and set the vertex and edge properties accordingly
# to the configuration file.
    def __init__(self):

        self.g = Graph()  # Create new graph object
        
        self.names = []
        self.contaminationCriteria = []
        self.count = 0

        self.read_data()
        self.add_vertex()
        self.add_edge()

    def read_data(self):
        # Read data from "dados_animais.txt" to set the graph properties
        ocorrencia = []
        dataFile = open("dados_animais.txt", "r", encoding='utf-8')

        for line in dataFile:
            if self.count != 0:
                self.names.append(line[:line.index('\t')])
                line = line[line.index('\t') + 1:]
                self.contaminationCriteria.append(line[:line.index('\t')])
                line = line[line.index('\t') + 1:]
                if line[len(line) - 1] == '\n':
                    ocorrencia.append(line[:len(line) - 1])
                else:
                    ocorrencia.append(line)
            self.count = self.count + 1

    def add_vertex(self):
        # Add vertex to the graph with the properties read from the file
        self.g.add_vertex(self.count - 1)

        vprop_name = self.g.new_vertex_property("string")  # Add properties to the vertex

        self.count = 0
        for name in self.names:  # Name the vertex
            vprop_name[self.count] = name
            self.count = self.count + 1

        self.g.vertex_properties["name"] = vprop_name  # Internalize de property "name"

        vprop_criterion = self.g.new_vertex_property("double")  # Add property to the vertices

        self.count = 0
        for value in self.contaminationCriteria:  # Define contamination criterion of vertices
            vprop_criterion[self.count] = float(value)
            self.count = self.count + 1

        self.g.vertex_properties[
            "contaminationCriteria"] = vprop_criterion  # Internalize the property "contaminationCriteria"

    def add_edge(self):
        # Create edges between vertices
        vprop_criterion = self.g.vertex_properties["contaminationCriteria"]
        eprop_criterion = self.g.new_edge_property("double")  # Add property to the edges

        for i in range(1, 8):
            self.g.add_edge(0, i)
            eprop_criterion[(0, i)] = vprop_criterion.a[0] / 10

        for i in range(1, 4):
            self.g.add_edge(6, i)
            eprop_criterion[(6, i)] = vprop_criterion.a[i] / 10
            self.g.add_edge(7, i)
            eprop_criterion[(7, i)] = vprop_criterion.a[i] / 10

        self.g.edge_properties["contaminationCriteria"] = eprop_criterion

    def get_graph(self):
            v_pos = self.g.new_vertex_property("vector<double>")
            for i in range(0,7,1):
                x = randint(0, 400)
                y = randint(0, 200)
                v_pos[self.g.vertex(i)] = [x, y]
            self.g.vertex_properties["position"] = v_pos

            return self.g
