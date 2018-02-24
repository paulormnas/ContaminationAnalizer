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

	def step_backward(self, graph):
		"""Start a backward step in SER algorithm and return the graph to be drawn"""
		return self.ser.run(g=graph, is_forward=False)

	def step_forward(self, graph):
		"""Start a forward step in SER algorithm and return the graph to be drawn"""
		return self.ser.run(g=graph, is_forward=True)

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

	def random_infect_specie(self, graph):
		self.ser.random_infect_specie(graph=graph)
