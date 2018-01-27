# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject
from graph_tool.all import *

import Control
import UpdateSpecies
import UpdateConnections
import gtk_graph_draw
import threading
import time

class CMainWindow(Gtk.Window):
	"""This class is responsable for create the main window of the application. All the containers, box and buttons
	are instaciated here."""

	def __init__(self):
		"""Start the controller and instantiate all the components of the Main Window"""
		self.ctrl = Control.CController()
		self.graph = self.ctrl.get_graph()
		self.sf = "shapefile/clipabaetetubasolo.shp"
		self.is_running = False # Attribute to control thread activity

		# Program main window.
		Gtk.Window.__init__(self, title="CSA") # CSA - Contamination Spreading Analyse
		# Get screen size and resize the program window to fill the screen.
		self.set_icon_from_file("icons/vertex.png")
		self.screen = self.get_screen()
		self.set_default_size(self.screen.get_width(), self.screen.get_height())
		self.connect("key-press-event", self.key_press_event)

		self.add_main_box()
		self.add_navigation_bar()
		self.add_horizontal_pane()
		self.add_project_view()
		self.add_notebook()
		self.add_statusbar()

	def add_main_box(self):
		"""First Box container in vertical orientation that hold the HeaderBar and the following layout containers"""
		self.vert_box = Gtk.Box(homogeneous=False,
		                        orientation='GTK_ORIENTATION_VERTICAL')
		self.add(self.vert_box)

	def add_navigation_bar(self):
		"""Add the navigation bar that show the buttons responsible by control the ERA engine."""
		self.navbar = Gtk.HeaderBar(spacing=50)

		# A box container to handle the buttons that allow configure the project properties
		config_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
		Gtk.StyleContext.add_class(config_box.get_style_context(), "linked")

		button = Gtk.Button()
		button.set_image(Gtk.Image.new_from_file("icons/species.png"))
		button.connect("clicked", self.update_species)
		config_box.add(button)

		button = Gtk.Button()
		button.set_image(Gtk.Image.new_from_file("icons/species.png"))
		button.connect("clicked", self.update_connections)
		config_box.add(button)

		# A Box container that is set inside the NavigationBar to handle the buttons that controls the simulator
		# iterations
		btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, homogeneous=True)
		Gtk.StyleContext.add_class(btn_box.get_style_context(), "linked")

		button = Gtk.Button()
		button.set_image(Gtk.Image.new_from_file("icons/step_backward.png"))
		button.connect("clicked", self.step_backward)
		btn_box.add(button)

		button = Gtk.Button()
		button.set_image(Gtk.Image.new_from_file("icons/step_forward.png"))
		button.connect("clicked", self.step_forward)
		btn_box.add(button)

		self.run_and_stop_btn = Gtk.Button()
		self.run_and_stop_btn.set_image(Gtk.Image.new_from_file("icons/run.png"))
		self.run_and_stop_btn.connect("clicked", self.run_continuously)
		btn_box.add(self.run_and_stop_btn)

		button = Gtk.Button()
		button.set_image(Gtk.Image.new_from_file("icons/reset.png"))
		button.connect("clicked", self.reset)
		btn_box.add(button)


		# Add a scale to adjust the speed of SER simulation
		adj = Gtk.Adjustment()
		adj.set_lower(1)
		adj.set_upper(100)
		adj.set_step_increment(2)
		adj.set_page_increment(10)
		self.scale = Gtk.Scale(orientation='GTK_ORIENTATION_HORIZONTAL', adjustment=adj)#
		self.scale.set_draw_value(False)
		self.scale.set_value(40)
		self.scale.set_hexpand(True)

		# Add icon to scale
		scl_img = Gtk.Image.new_from_file("icons/speed.png")

		# New box to handle the scale and it's icon
		scl_box = Gtk.Box(orientation='GTK_ORIENTATION_HORIZONTAL', homogeneous=False)
		scl_box.pack_start(scl_img, False, False, 0)
		scl_box.pack_start(self.scale, True, True, 0)

		# New box to handle the button's box and scale's box and add space between then
		hb_box_sim = Gtk.Box(orientation='GTK_ORIENTATION_HORIZONTAL', homogeneous=True, spacing=20)
		hb_box_sim.pack_start(btn_box, True, False, 0)
		hb_box_sim.pack_start(scl_box, True, True, 0)

		# New box to handle the configuration buttons and separete then from the buttons that controls the simulation
		hb_box_config = Gtk.Box(orientation='GTK_ORIENTATION_HORIZONTAL', homogeneous=True, spacing=20)
		hb_box_config.add(config_box)

		# Pack the boxes into Navigation Bar
		self.navbar.pack_start(hb_box_config)
		self.navbar.pack_start(hb_box_sim)

		# Pack the Navigation Bar at the start of the main vertical box
		self.vert_box.pack_start(self.navbar, False, False, 0)

	def add_horizontal_pane(self):
		"""A Paned container with horizontal orientation that handle the notebook and project view"""
		self.horizontal_pane = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
		self.vert_box.pack_start(self.horizontal_pane, True, True, 0)

	def add_project_view(self):
		"""Create a porject view composed by a header and a ListBox that show the structure of itens present
		in the project"""
		self.project_view_box = Gtk.Box(homogeneous=False,
		                                orientation=Gtk.Orientation.VERTICAL)
		self.horizontal_pane.add1(self.project_view_box)

		# Add a header to the project view with controls
		hb = Gtk.Box(homogeneous=False,
		             orientation=Gtk.Orientation.HORIZONTAL,
		             spacing=2)
		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		hb.pack_end(button, False, True, 0)
		self.project_view_box.pack_start(hb, False, True, 0)

		# A Box container that is set inside the NavigationBar to handle the buttons
		project_hb_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(project_hb_box.get_style_context(), "linked")

		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
		project_hb_box.add(button)

		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
		project_hb_box.add(button)

		hb.pack_start(project_hb_box, False, False, 0)

		# Add the ListBox with project itens information
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		self.project_view_box.pack_end(listbox, True, True, 0)

		for name in self.graph.vertex_properties["species"]:
			exp = Gtk.Expander()
			exp.set_label_widget(self.project_view_item_label(label=[name],
			                                                  icon="vertex"))
			row = Gtk.ListBoxRow()
			row.add(exp)
			listbox.add(row)
		# animals = self.ctrl.get_animals()
		#
		# for a in animals:
		# 	exp = Gtk.Expander()
		# 	exp.set_label_widget(self.project_view_item_label(label=[a["species"]],
		# 	                                                  icon="vertex"))
		#
		# 	spread_models = "\t\tSpread Model: "
		# 	for sm in a["spread_model"]:
		# 		spread_models = spread_models + str(sm) + " "
		#
		# 	group = "\t\tTc Group: "
		# 	for g in a["group"]:
		# 		group = group + str(g) + " "
		#
		# 	habitat = "\t\tHabitat: "
		# 	for h in a["habitat"]:
		# 		habitat = habitat + str(h) + " "
		# 	exp.add(self.project_view_item_label(label=[spread_models, group, habitat]))
		#
		# 	row = Gtk.ListBoxRow()
		# 	row.add(exp)
		# 	listbox.add(row)
		listbox.show_all()

	def project_view_item_label(self, label=None, icon=None):
		"""This function is used to construct the label of the items in the project view"""
		vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
		                  homogeneous=False,
		                  spacing=6)

		for l in label:
			item_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
			                   homogeneous=False,
			                   spacing=6)
			item_label = Gtk.Label()
			item_label.set_text(l)
			if len(label) > 1:
				item_label.set_markup("""<span foreground="blue">""" + l + "</span>")

			if icon is not None:
				item_icon = Gtk.Image.new_from_file("icons/" + icon + ".png")
				item_box.add(item_icon)

			item_box.pack_start(item_label, False, False, 6)
			vbox.add(item_box)

		return vbox

	def add_notebook(self):

		self.nb = Gtk.Notebook()

		self.page_environment = Gtk.Overlay()

		self.graph_widget = gtk_graph_draw.GraphWidgetWithBackImage(self.graph,
		                                                       pos=self.graph.vertex_properties["position"],
		                                                       vertex_size=80,
		                                                       vertex_text=self.graph.vertex_properties.species,
		                                                       vertex_text_position=-5,
		                                                       vertex_font_size=12,
		                                                       # edge_pen_width=self.graph.edge_properties["contaminationCriteria"],
		                                                       geometry=(self.screen.get_width, self.screen.get_height),
		                                                       edge_marker_size=30,
		                                                       bg_color=[1, 1, 1, 0],
		                                                       bg_image=self.sf) #Only shapefiles are accepted

		self.page_environment.add_overlay(self.graph_widget)
		# self.page_environment.add(Gtk.Label('Environment simulation page'))
		self.nb.append_page(self.page_environment, Gtk.Label('Environment'))

		self.page_plot = Gtk.Box()
		self.page_plot.set_border_width(10)
		self.page_plot.add(Gtk.Label('A page with an image for a Title.'))
		self.nb.append_page(self.page_plot,
		                    Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
		                    )

		self.horizontal_pane.add2(self.nb)

	def add_statusbar(self):
		"""Add a status bar on the bottom of the window."""
		self.sb = Gtk.Statusbar()
		self.context_id = self.sb.get_context_id("__iteration__")
		self.vert_box.pack_end(self.sb, False, False, 0)


	def key_press_event(self, widget, event):
		"""Handle key press."""

		# If the page_environment is displayed than handle the event key inside graph_widget
		if self.nb.get_current_page() == 0:
			self.graph_widget.key_press_event(self.graph_widget, event=event)

	def redraw(self):
		"""Redraw the graph in environment page and show the number of iterations executed by the SER simulation"""
		self.graph_widget.regenerate_surface(reset=True)
		self.graph_widget.queue_draw()
		self.sb.push(self.context_id,
		             "Iteration: " + str(self.ctrl.get_iterations()) + "   " +
		             "Speed: " + str(round(self.scale.get_value(), 0)) + "%   ")

	def step_backward(self, widget):
		"""Execute one step backward in SER simulation"""
		if not self.is_running:
			self.graph = self.ctrl.step_backward(self.graph)
			self.redraw()

	def step_forward(self, widget):
		"""Execute one step forward in SER simulation"""
		if not self.is_running:
			self.graph = self.ctrl.step_forward(self.graph)
			self.redraw()

	def run_continuously(self, widget):
		"""Start a thread to run step forward continuously"""
		if not self.is_running:
			self.is_running = True
			t = threading.Thread(target=self.threaded_step_forward)
			t.start()
			self.run_and_stop_btn.set_image(Gtk.Image.new_from_file("icons/stop.png"))
		else:
			self.is_running = False
			self.run_and_stop_btn.set_image(Gtk.Image.new_from_file("icons/run.png"))

	def threaded_step_forward(self):
		"""Execute step forward continuously in SER simulation inside a thread"""
		while self.is_running:
			self.graph = self.ctrl.step_forward(self.graph)
			GObject.idle_add(self.redraw)
			time.sleep(3 / self.scale.get_value())

	def reset(self, widget):
		"""Reset the SER simulation"""
		if not self.is_running:
			self.graph = self.ctrl.reset(self.graph)
			self.redraw()

	def update_species(self, widget):
		"""Open new window to edit species properties"""
		win = UpdateSpecies.CUpdateSpecies()
		win.show_all()
		win.set_keep_above(True)

	def update_connections(self, widget):
		"""Open new window to edit species properties"""
		win = UpdateConnections.CUpdateConnections()
		win.show_all()
		win.set_keep_above(True)