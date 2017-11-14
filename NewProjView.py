# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject
from graph_tool.all import *

import Control


class CUpdateSpecies(Gtk.Window):
	def __init__(self, path=None):
		self.ctrl = Control.CController()

		# New window to add and update the species properties in the project.
		Gtk.Window.__init__(self,
		                    title="Update Species")
		# Get screen size and resize the program window to fill the screen.
		self.set_default_size(600, 600)
		self.set_position(Gtk.WindowPosition(1)) # 1 = GTK_WIN_POS_CENTER

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
		self.hbox.add(tree_box)

		tree_description = Gtk.Label("Species already added to the project.")
		tree_box.pack_start(tree_description, False, False, 0)

		self.tv = Gtk.TreeView()
		tree_box.pack_end(self.tv, False, False, 0)

	def add_properties_options(self):
		# Create the right part of the window with the structure to edit the species properties
		prop_box = Gtk.Box(homogeneous=False,
		                    orientation='GTK_ORIENTATION_VERTICAL')
		self.hbox.add(prop_box)

		# Add label and text editor for the species name
		name_box = Gtk.Box(homogeneous=False,
		                   orientation='GTK_ORIENTATION_HORIZONTAL',
		                   spacing=10)
		prop_box.pack_start(name_box, True, False, 0)

		name_label = Gtk.Label("Species name")
		name_box.pack_start(name_label, False, False, 0)

		self.name_entry = Gtk.Entry()
		self.name_entry.set_editable(True)
		name_box.pack_end(self.name_entry, False, False, 0)

		# Horizontal box that handle the Habitat and Tc Group properties
		hbox = Gtk.Box(homogeneous=False,
		               orientation='GTK_ORIENTATION_HORIZONTAL',
		               spacing=20)
		prop_box.pack_end(hbox, False, False, 0)

		vbox = Gtk.Box(homogeneous=False,
		               orientation='GTK_ORIENTATION_VERTICAL',
		               spacing=10)
		habitat_label = Gtk.Label("Habitats")
		habitat_tree = Gtk.TreeView()
		vbox.add(habitat_label)
		vbox.add(habitat_tree)
		hbox.add(vbox)

		vbox = Gtk.Box(homogeneous=False,
		               orientation='GTK_ORIENTATION_VERTICAL',
		               spacing=10)
		group_label = Gtk.Label("Tc group and Spread Models")
		group_tree = Gtk.TreeView()
		vbox.add(group_label)
		vbox.add(group_tree)
		hbox.add(vbox)

	def load_from_file(self):
		pass
