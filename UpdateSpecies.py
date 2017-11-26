# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk, GObject

import Control

class CUpdateSpecies(Gtk.Window):
	"""This class is responsible to present the user a GUI that allows to configure the existing species in the
	simulation and their properties. Those properties are: Tripanossoma Cruzi (Tc) group that a species can be infected,
	the spread model used by each Tc group to spread the contamination between species and the habitat where those
	species live. All those properties are saved in a JSON file which will be used later to construct the graph of the
	simulation"""

	PADDING = 12  # Constant value used to add padding on Gtk.Widgets

	def __init__(self):
		self.ctrl = Control.CController()
		self.species = self.ctrl.get_species()      # Load species data from species.json

		# New window to add and update the species properties in the project.
		Gtk.Window.__init__(self, title="Update Species")

		# Get screen size and resize the program window to fill the screen.
		self.set_default_size(400, 400)
		self.set_position(Gtk.WindowPosition(1))    # 1 = GTK_WIN_POS_CENTER

		self.add_main_box()
		self.add_species_list()
		self.add_properties_options()
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
		"""Add a ListBox to the window that will help to see the species already added to the project"""
		list_box = Gtk.Box(homogeneous=False,
		                   orientation='GTK_ORIENTATION_VERTICAL',
		                   spacing=0)
		self.hbox.pack_start(list_box, True, False, self.PADDING)

		list_description = Gtk.Label("Species already added to the project.")
		list_box.pack_start(list_description, False, False, self.PADDING)

		self.listbox = Gtk.ListBox()
		self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
		list_box.pack_start(self.listbox, True, True, self.PADDING)

		self.populate_species_list()

	def populate_species_list(self):
		"""Clean the ListBox and populate it with the species properties from the self.species dictionary"""
		for row in self.listbox.get_children():
			self.listbox.remove(row)

		for a in self.species:
			exp = Gtk.Expander()
			exp.connect("activate", self.on_expander_selected)
			exp.set_label(a["species"])

			spread_models = "\tSpread Model: "
			for sm in a["spread_model"]:
				spread_models = spread_models + str(sm) + " "

			group = "\tTc Group: "
			for g in a["group"]:
				group = group + str(g) + " "

			habitat = "\tHabitat: "
			for h in a["habitat"]:
				habitat = habitat + str(h) + " "
			exp.add(self.species_list_items(label=[spread_models, group, habitat]))

			row = Gtk.ListBoxRow()
			row.add(exp)
			self.listbox.add(row)
		self.listbox.show_all()

	def species_list_items(self, label=None, icon=None):
		# This function is used to construct the label of the items in the project view
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

			if icon == "vertex":
				item_icon = Gtk.Image.new_from_file("icons/vertex.png")
				item_box.add(item_icon)

			item_box.pack_start(item_label, False, False, 6)
			vbox.add(item_box)

		return vbox

	def add_properties_options(self):
		"""Create the right part of the window with the structure to edit the species properties"""
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
		prop_box.pack_start(hbox, True, True, 0)

		# Create habitat options
		vbox = Gtk.Box(homogeneous=False,
		               orientation='GTK_ORIENTATION_VERTICAL',
		               spacing=10)

		self.habitat_sto = Gtk.ListStore(str, bool)
		habitats = self.ctrl.get_habitats()
		for h in habitats:
			self.habitat_sto.append([h, False])

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

		vbox.pack_start(habitat_tree, True, True, self.PADDING)
		hbox.add(vbox)

		# Create Tc group and Spread models options
		vbox = Gtk.Box(homogeneous=False,
		               orientation='GTK_ORIENTATION_VERTICAL',
		               spacing=10)

		self.spread_model_sto = Gtk.ListStore(str)
		models = self.ctrl.get_spread_models()
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
		self.select = group_tree.get_selection()
		self.select.set_mode(1)  # 1 = Single

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

		vbox.pack_start(group_tree, True, True, self.PADDING)
		hbox.add(vbox)

	def add_buttons(self):
		"""Add buttons to the bottom of the window"""
		btn_box = Gtk.Box(homogeneous=False,
		                  orientation='GTK_ORIENTATION_HORIZONTAL',
		                  spacing=10)
		self.vbox.pack_end(btn_box, False, False, self.PADDING)

		# Box to organize the UPDATE and DELETE buttons at the bottom of the window
		upd_del_box = Gtk.Box(homogeneous=True,
		                        orientation='GTK_ORIENTATION_HORIZONTAL',
		                        spacing=10)
		btn_box.pack_start(upd_del_box, False, False, self.PADDING)

		update_btn = Gtk.Button(label="Update")
		update_btn.connect("button-release-event", self.update_species_list)
		upd_del_box.pack_start(update_btn, True, True, self.PADDING)

		delete_btn = Gtk.Button(label="Delete")
		delete_btn.connect("button-release-event", self.delete_species_from_list)
		upd_del_box.pack_start(delete_btn, True, True, self.PADDING)

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

	def on_habitat_cell_toggled(self, widget, path):
		"""Just change the state of habitat toggle when the user click on it"""
		self.habitat_sto[path][1] = not self.habitat_sto[path][1]

	def on_group_cell_toggled(self, widget, path):
		"""Just change the state of Tc group toggle when the user click on it"""
		self.group_sto[path][1] = not self.group_sto[path][1]

	def on_group_combo_changed(self, widget, path, text):
		"""Change the combo to the value selected by the user and unselect the row"""
		self.group_sto[path][2] = text
		self.select.unselect_all()

	def on_expander_selected(self, widget):
		"""When the expander is selected the properties list is updated with the data of the respective animal"""
		if widget.get_expanded:
			for a in self.species:
				if a["species"] == widget.get_label():
					self.update_properties_lists(species_prop=a)

	def update_properties_lists(self, species_prop):
		"""Update the species properties options, in the right side of the window, with the data of the species selected
		by the user from the list in the left side of the window"""
		self.name_entry.set_text(species_prop["species"])

		for row in self.habitat_sto:
			if row[0] in species_prop["habitat"]:
				row[1] = True
			else:
				row[1] = False

		for row in self.group_sto:
			if row[0] in species_prop["group"]:
				row[1] = True
				index = species_prop["group"].index(row[0])
				row[2] = species_prop["spread_model"][index]
			else:
				row[1] = False
				row[2] = "SI"

	def update_species_list(self, widget, event):
		"""Update the species list in the right side of the window with the properties information provided by the user."""
		habitats = []
		for row in self.habitat_sto:
			if row[1]:
				habitats.append(row[0])

		group = []
		spread_model = []
		for row in self.group_sto:
			if row[1]:
				group.append(row[0])
				spread_model.append(row[2])

		exist = False
		for a in self.species:
			if self.name_entry.get_text() == a["species"]:
				exist = True
				a["habitat"] = habitats
				a["group"] = group
				a["spread_model"] = spread_model

		if not exist:
			a = {"species": self.name_entry.get_text(),
			     "habitat": habitats,
			     "group": group,
			     "spread_model": spread_model}
			self.species.append(a)

		self.populate_species_list()

	def delete_species_from_list(self, widget, event):
		"""Remove the species selected by the user from the list"""
		for a in self.species:
			if self.name_entry.get_text() == a["species"]:
				self.species.remove(a)
		self.populate_species_list()

	def cancel_clicked(self, widget, event):
		"""Just close the window and cancel the operation without saving the modifications"""
		self.close()

	def ok_clicked(self, widget, event):
		"""Close the window and save the modification to the species properties on species.json file"""
		self.ctrl.save_species_list(data=self.species)
		self.close()
