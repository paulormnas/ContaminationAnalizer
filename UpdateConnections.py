# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import Control

class CUpdateConnections(Gtk.Window):
	"""This class is responsible for create the window that allow the user configure the connections between the animals
	species. This connections will be used later to construct the graph that will be used in simulation. After the
	modification, if the user click on OK button all modifications are saved at connections.json file, otherwise the file
	remains intact and the connections will stay in the initial state."""

	PADDING = 12  # Constant value used to add padding on Gtk.Widgets

	def __init__(self):
		self.ctrl = Control.CController()
		self.species = self.ctrl.get_species()  # Load species data from species.json
		self.connections = self.ctrl.get_connections()  # Load list with the connections between species from connections.json
		self.selected = None

		# New window to add and update the species properties in the project.
		Gtk.Window.__init__(self, title="Update Connections")

		# Get screen size and resize the program window to fill the screen.
		self.set_default_size(400, 400)
		self.set_position(Gtk.WindowPosition(1))  # 1 = GTK_WIN_POS_CENTER

		self.add_main_box()
		self.add_species_list()
		self.add_connections_options()
		self.add_buttons()

	def add_main_box(self):
		"""Here the first box container is added in vertical orientation and your role is handle all the window layout.
		 A second box container is also added but in horizontal orientation, which handle the lists layout"""
		self.vbox = Gtk.Box(homogeneous=False,
		                    orientation='GTK_ORIENTATION_VERTICAL',
		                    spacing=0)

		self.hbox = Gtk.Box(homogeneous=False,
		                    orientation='GTK_ORIENTATION_HORIZONTAL',
		                    spacing=10)

		self.vbox.pack_start(self.hbox, True, True, 0)
		self.add(self.vbox)

	def add_species_list(self):
		"""Add a ListBox to the window that will help to see the species in the project"""
		l_box = Gtk.Box(homogeneous=False,
		                orientation='GTK_ORIENTATION_VERTICAL',
		                spacing=10)
		self.hbox.pack_start(l_box, True, True, self.PADDING)

		self.listbox = Gtk.ListBox()
		self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
		l_box.pack_start(self.listbox, True, True, self.PADDING)

		self.populate_species_list()

	def populate_species_list(self):
		"""Clean the ListBox and populate it with the species properties from the self.animals dictionary"""
		for row in self.listbox.get_children():
			self.listbox.remove(row)

		for s in self.species:
			exp = Gtk.Expander()
			exp.set_label(s["species"])
			exp.connect("activate", self.on_expander_selected)
			row = Gtk.ListBoxRow()
			row.add(exp)
			self.listbox.add(row)

		row = self.listbox.get_row_at_index(0)
		self.selected = row.get_child().get_label()

		self.listbox.show_all()

	def add_connections_options(self):
		"""Create the right part of the window with the structure to edit the species connections"""
		connection_box = Gtk.Box(homogeneous=False,
		                         orientation='GTK_ORIENTATION_VERTICAL',
		                         spacing=6)
		self.hbox.pack_start(connection_box, True, False, self.PADDING)

		# Create the list with the species to create a connection
		self.connections_sto = Gtk.ListStore(str, bool)
		for s in self.species:
			self.connections_sto.append([s["species"], False])

		species_tree = Gtk.TreeView(model=self.connections_sto)
		select = species_tree.get_selection()
		select.set_mode(0) # 0 = None

		renderer_text = Gtk.CellRendererText()
		column_text = Gtk.TreeViewColumn("Species", renderer_text, text=0)
		species_tree.append_column(column_text)

		renderer_toggle = Gtk.CellRendererToggle()
		renderer_toggle.connect("toggled", self.on_connect_cell_toggled)
		column_toggle = Gtk.TreeViewColumn("Connect to", renderer_toggle, active=1)
		species_tree.append_column(column_toggle)

		connection_box.pack_start(species_tree, True, True, self.PADDING)
		self.update_connections_list(self.selected)

	def add_buttons(self):
		"""Add buttons to the bottom of the window"""
		btn_box = Gtk.Box(homogeneous=False,
		                  orientation='GTK_ORIENTATION_HORIZONTAL',
		                  spacing=10)

		self.vbox.pack_end(btn_box, False, False, self.PADDING)

		# Box to organize the OK and CANCEL buttons at the bottom of the window
		ok_cancel_box = Gtk.Box(homogeneous=True,
		                        orientation='GTK_ORIENTATION_HORIZONTAL',
		                        spacing=10)
		btn_box.pack_end(ok_cancel_box, False, False, self.PADDING)

		ok_btn = Gtk.Button(label="OK")
		ok_btn.connect("button-release-event", self.ok_clicked)
		ok_cancel_box.pack_end(ok_btn, True, True, self.PADDING)

		cancel_btn = Gtk.Button(label="Cancel")
		cancel_btn.connect("button-release-event", self.cancel_clicked)
		ok_cancel_box.pack_end(cancel_btn, True, True, self.PADDING)

	def on_connect_cell_toggled(self, widget, path):
		"""If the user select a new connection, so the program add the species selected to the list of connections. Else,
		the program remove it from the list."""

		self.connections_sto[path][1] = not self.connections_sto[path][1]
		if self.connections_sto[path][1]:
			self.connections[self.selected].append(self.connections_sto[path][0])
		elif self.connections_sto[path][0] in self.connections[self.selected]:
			self.connections[self.selected].remove(self.connections_sto[path][0])

	def on_expander_selected(self, widget):
		"""Get the name of the selected species and update the connections list"""
		widget.set_expanded(True)
		self.selected = widget.get_label()
		self.update_connections_list(widget.get_label())

	def update_connections_list(self, name):
		"""Update the state of the toggles on connections list accordingly to the species specified by @name"""
		for row in self.connections_sto:
			if row[0] in self.connections[name]:
				row[1] = True
			else:
				row[1] = False

	def cancel_clicked(self, widget, event):
		"""Just close the window and cancel the operation without saving the modifications"""
		self.close()

	def ok_clicked(self, widget, event):
		"""Close the window and save the modification to the connections on connections.json file"""
		self.ctrl.save_connections_list(data=self.connections)
		self.close()