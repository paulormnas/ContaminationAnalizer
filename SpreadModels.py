# coding=utf-8
from graph_tool.all import *
from numpy.random import *
import numpy

_colors_defaults = {
    "S": (186 / 255, 172 / 255, 18 / 255, 0.8),
    "I": (196 / 255, 23 / 255, 23 / 255, 0.8),
    "R": (47 / 255, 174 / 255, 8 / 255, 0.8),
    "IM": (8 / 255, 47 / 255, 208 / 255, 0.8)
}


class CSIR:
    def __init__(self):
        # SIRS dynamics parameters:
        self.x = 0.1  # spontaneous outbreak probability
        self.r = 0.001  # I->R probability
        self.s = 0.1  # R->S probability
        self.sinks = []

    @staticmethod
    def get_state_color(state):
        return _colors_defaults[state]

    def random_infect(self, g, grp):
        """
        Choose a random vertex to change it's state to infected and update it's properties
        :param g: The graph used o simulation
        :type g: graph_tool.Graph
        :param grp: The graph used o simulation
        :type grp: str
        :return: None
        :rtype: None
        """
        trials = 0
        while trials <= g.num_vertices():
            v_index = randint(0, g.num_vertices() - 1)
            v = g.vertex(v_index)
            if grp in g.vertex_properties.group[v]:
                group_list = list(g.vertex_properties.group[v])
                index = group_list.index(grp)
                if g.vertex_properties.state[v][index] is "I":
                    trials += 1
                else:
                    g.vertex_properties.state_color[v] = self.get_state_color("I")
                    g.vertex_properties.state[v][index] = "I"
                    break
            else:
                trials += 1

    def infect(self, graph, group_observed, index, source, is_forward, vertex_states, iteration):
        group = graph.vertex_properties.group[source][index]  # Identify the type of Tc
        if is_forward:
            # If is a simulation step forward, than the infection spread from source to out neighbors, respecting the
            # spread model of each group.
            neighbors_list = graph.get_out_neighbors(source)
            for n in neighbors_list:
                if group in graph.vertex_properties.group[n]:
                    group_list = list(graph.vertex_properties.group[n])
                    n_index = group_list.index(group)
                    is_observed = group_observed == group
                    if graph.vertex_properties.spread_model[n][n_index] == "SI":
                        # Infect neighbor using SI model
                        self.si(graph=graph,
                                s=source,
                                v=n,
                                s_index=index,
                                v_index=n_index,
                                is_observed=is_observed)
                    if graph.vertex_properties.spread_model[n][n_index] == "SIS":
                        # Infect neighbor using SIS model
                        self.sis(graph=graph,
                                 s=source,
                                 v=n,
                                 s_index=index,
                                 v_index=n_index,
                                 is_observed=is_observed)
                    if graph.vertex_properties.spread_model[n][n_index] == "SIR":
                        # Infect neighbor using SIR model
                        self.sir(graph=graph,
                                 s=source,
                                 v=n,
                                 s_index=index,
                                 v_index=n_index,
                                 is_observed=is_observed)
        else:
            neighbors_list = graph.get_in_neighbors(source)
            for n in neighbors_list:
                if group in graph.vertex_properties.group[n]:
                    group_list = list(graph.vertex_properties.group[n])
                    n_index = group_list.index(group)
                    # If is a simulation step backward, than recover the state of each neighbor on last iteration
                    states = vertex_states[iteration]
                    state = states[graph.vertex_index[n]]
                    graph.vertex_properties.state[n][n_index] = state[n_index]
                    # Identify the group of Tc observed by the user and change the vertex color accordingly
                    is_observed = group_observed == group
                    if is_observed:
                        graph.vertex_properties.state_color[n] = self.get_state_color(state[n_index])

    def si(self, graph, s, v, s_index, v_index, is_observed):
        if random() < self.x and graph.vertex_properties.state[s][s_index] == "I" and \
                graph.vertex_properties.state[v][v_index] == "S":
            graph.vertex_properties.state[v][v_index] = "I"
            if is_observed:
                graph.vertex_properties.state_color[v] = self.get_state_color("I")

    def sis(self, graph, s, v, s_index, v_index, is_observed):
        if graph.vertex_properties.state[s][s_index] == "I":
            if random() < self.x and graph.vertex_properties.state[v][v_index] == "S":
                graph.vertex_properties.state[v][v_index] = "I"
                if is_observed:
                    graph.vertex_properties.state_color[v] = self.get_state_color("I")
            if random() < self.s:
                graph.vertex_properties.state[v][v_index] = "S"
                if is_observed:
                    graph.vertex_properties.state_color[v] = self.get_state_color("S")

    def sir(self, graph, s, v, s_index, v_index, is_observed):
        if graph.vertex_properties.state[s][s_index] == "I":
            if random() < self.x and graph.vertex_properties.state[v][v_index] == "S":
                graph.vertex_properties.state[v][v_index] = "I"
                if is_observed:
                    graph.vertex_properties.state_color[v] = self.get_state_color("I")
            if random() < self.r:
                graph.vertex_properties.state[v][v_index] = "R"
                if is_observed:
                    graph.vertex_properties.state_color[v] = self.get_state_color("R")
