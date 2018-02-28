# coding=utf-8
import test_graph
import SER
import LoadData
import SaveData

class CController():
	"""
	This class is used to conect que View class to the others. It is a intermediate class responsible for manage
	the information transit between classes.
	"""
	def __init__(self):
		"""Instantiate the classes that will be controlled by CController"""
		self.ser = SER.CSER()
		self.ld = LoadData.CLoadData()
		self.sd = SaveData.CSaveData()

		self.env_graph = test_graph.CEnvironmentGraph(species=self.ld.read_species(),
		                                              connections=self.ld.read_connections())
		self.graph = self.env_graph.get_graph()

	def get_graph(self):
		"""Get the graph that will be drawn in the environment page"""
		return self.env_graph.get_graph()

	def set_shapefile(self, sf):
		self.env_graph.read_shapes(sf)

	def update_widget_dim(self, w_width, w_height, w_pos_x, w_pos_y):
		self.env_graph.update_dimensions(w_width, w_height, w_pos_x, w_pos_y)

	def gen_graph(self):
		self.env_graph.gen_graph()

	def get_iterations(self):
		return self.ser.get_iterations_number()

	def step_backward(self, graph, group_observed):
		"""Start a backward step in SER algorithm and return the graph to be drawn"""
		return self.ser.run(g=graph, is_forward=False, go=group_observed)

	def step_forward(self, graph, group_observed):
		"""Start a forward step in SER algorithm and return the graph to be drawn"""
		return self.ser.run(g=graph, is_forward=True, go=group_observed)

	def reset(self, graph):
		"""Reset the SER algorithm for the initial state and return the graph to be drawn"""
		return self.ser.reset(g=graph)

	def get_spread_models(self):
		"""Use object from class LoadData to access configuration JSON file and retrieve the spread models"""
		return self.ld.read_spread_models()

	def get_habitats(self):
		"""Use object from class LoadData to access configuration JSON file and retrieve the habitats"""
		return self.ld.read_habitats()

	def get_species(self):
		"""Use object from class LoadData to access configuration JSON file and retrieve the species and
		their properties"""
		return self.ld.read_species()

	def save_species_list(self, data):
		"""Use object from class SaveData to write species and their properties to JSON file"""
		self.sd.save_species(data=data)

	def get_connections(self):
		"""Use object from class LoadData to access configuration JSON file and retrieve the connections for
		each species"""
		return self.ld.read_connections()

	def save_connections_list(self, data):
		"""Use object from class SaveData to write connections specifications of each species to JSON file"""
		self.sd.save_connections(data=data)

	def random_infect_specie(self, graph, group):
		"""
		Choose a vertex randomly and change it state to infected for the selected Tc group
		:param graph: Graph use created for the simulation
		:type graph: graph_tool.Graph
		:param group: Tc group selected by the user
		:type group: str
		:return: None
		:rtype: None
		"""
		self.ser.random_infect_specie(graph=graph, group=group)

	def get_available_groups(self):
		"""
		Verify what groups of Tc is used by the graph model and specified on configuration files
		:return: List of strings with all Tc groups that can infect the animals on model
		:rtype: list
		"""
		return self.env_graph.get_groups()

	def update_color_state(self, group):
		"""
		Update the colors of the graph to represent the species state accordingly to the Tc group selected by the user
		:param group: Tc group selected using the group combobox
		:type group: str
		:return: None
		:rtype: None
		"""
		self.env_graph.upd_state(group)
