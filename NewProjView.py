# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject
from graph_tool.all import *

import Control


class CUpdateSpecies(Gtk.Window):
	PADDING = 12  # Constant value used to add padding on Gtk.Widgets

	def __init__(self, path=None):
		self.ctrl = Control.CController()

		# New window to add and update the species properties in the project.
		Gtk.Window.__init__(self,
		                    title="Update Species")
		# Get screen size and resize the program window to fill the screen.
		self.set_default_size(600, 600)
		self.set_position(Gtk.WindowPosition(1))    # 1 = GTK_WIN_POS_CENTER

		self.add_main_box()
		self.add_tree_view()
		self.add_properties_options()

		if path is not None:
			self.load_from_file()

	def add_main_box(self):
		# First Box container in horizontal orientation that hold the remain os the layout
		self.hbox = Gtk.Box(homogeneous=False,
		                    orientation='GTK_ORIENTATION_HORIZONTAL',
		                    spacing=10)
		self.add(self.hbox)

	def add_tree_view(self):
		# Add a TreeView to the window that will help to see the species already added to the project
		tree_box = Gtk.Box(homogeneous=False,
		                   orientation='GTK_ORIENTATION_VERTICAL',
		                   spacing=10)
		self.hbox.pack_start(tree_box, True, False, self.PADDING)

		tree_description = Gtk.Label("Species already added to the project.")
		tree_box.pack_start(tree_description, False, False, self.PADDING)

		self.tv = Gtk.TreeView()
		tree_box.pack_start(self.tv, False, False, self.PADDING)

	def add_properties_options(self):
		# Create the right part of the window with the structure to edit the species properties
		prop_box = Gtk.Box(homogeneous=False,
		                   orientation='GTK_ORIENTATION_VERTICAL',
		                   spacing=6)
		self.hbox.pack_start(prop_box, True, False, self.PADDING)

		# Add label and text editor for the species name
		name_box = Gtk.Box(homogeneous=False,
		                   orientation='GTK_ORIENTATION_HORIZONTAL',
		                   spacing=20)
		prop_box.pack_start(name_box, False, False, self.PADDING)

		name_label = Gtk.Label("Species name:")
		name_box.pack_start(name_label, False, False, 0)

		self.name_entry = Gtk.Entry()
		self.name_entry.set_editable(True)
		name_box.pack_end(self.name_entry, True, True, 0)

		# Horizontal box that handle the Habitat and Tc Group properties
		hbox = Gtk.Box(homogeneous=False,
		               orientation='GTK_ORIENTATION_HORIZONTAL',
		               spacing=20)
		prop_box.pack_start(hbox, True, True, self.PADDING)

		# Create habitat options
		vbox = Gtk.Box(homogeneous=False,
		               orientation='GTK_ORIENTATION_VERTICAL',
		               spacing=10)
		habitat_label = Gtk.Label("Habitats")

		self.habitat_sto = Gtk.ListStore(str, bool)
		self.habitat_sto.append(["Forest", False])
		self.habitat_sto.append(["Grass", False])
		self.habitat_sto.append(["Water", False])
		self.habitat_sto.append(["City", False])

		habitat_tree = Gtk.TreeView(model=self.habitat_sto)
		select = habitat_tree.get_selection()
		select.set_mode(0) # 0 = None

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Habitat", renderer_text, text=0)
		habitat_tree.append_column(column_text)

		renderer_toggle = Gtk.CellRendererToggle()
		renderer_toggle.connect("toggled", self.on_habitat_cell_toggled)
		column_toggle = Gtk.TreeViewColumn("Live in", renderer_toggle, active=1)
		habitat_tree.append_column(column_toggle)

		vbox.add(habitat_label)
		vbox.pack_start(habitat_tree, True, True, self.PADDING)
		hbox.add(vbox)

		# Create Tc group and Spread models options
		vbox = Gtk.Box(homogeneous=False,
		               orientation='GTK_ORIENTATION_VERTICAL',
		               spacing=10)
		group_label = Gtk.Label("Tc group and Spread Models")

		self.spread_model_sto = Gtk.ListStore(str)
		models = ["SI", "SIS", "SIR"]
		for item in models:
			self.spread_model_sto.append([item])

		self.group_sto = Gtk.ListStore(str, bool, str)
		self.group_sto.append(["TcI", False, "SI"])
		self.group_sto.append(["TcII", False, "SI"])
		self.group_sto.append(["TcIII", False, "SI"])
		self.group_sto.append(["TcIV", False, "SI"])
		self.group_sto.append(["TcV", False, "SI"])
		self.group_sto.append(["TcVI", False, "SI"])
		self.group_sto.append(["TcVII", False, "SI"])

		group_tree = Gtk.TreeView(model=self.group_sto)
		select = group_tree.get_selection()
		select.set_mode(0)  # 0 = None

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Group", renderer_text, text=0)
		group_tree.append_column(column_text)

		renderer_toggle = Gtk.CellRendererToggle()
		renderer_toggle.connect("toggled", self.on_group_cell_toggled)
		column_toggle = Gtk.TreeViewColumn("Is present", renderer_toggle, active=1)
		group_tree.append_column(column_toggle)

		renderer_combo = Gtk.CellRendererCombo()
		renderer_combo.set_property("editable", True)
		renderer_combo.set_property("model", self.spread_model_sto)
		renderer_combo.set_property("text-column", 0)
		renderer_combo.set_property("has-entry", False)
		renderer_combo.connect("edited", self.on_group_combo_changed)

		column_combo = Gtk.TreeViewColumn("Spread Model", renderer_combo, text=2)
		group_tree.append_column(column_combo)

		vbox.add(group_label)
		vbox.pack_start(group_tree, True, True, self.PADDING)
		hbox.add(vbox)

	def on_habitat_cell_toggled(self, widget, path):
		self.habitat_sto[path][1] = not self.habitat_sto[path][1]

	def on_group_cell_toggled(self, widget, path):
		self.group_sto[path][1] = not self.group_sto[path][1]

	def on_group_combo_changed(self, widget, path, text):
		self.spread_model_sto[path][2] = text

	def load_from_file(self):
		pass
