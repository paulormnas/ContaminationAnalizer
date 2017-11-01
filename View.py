# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from graph_tool.all import *

import Control, gtk_graph_draw

class CMainWindow(Gtk.Window):
# This class is used to create the main window of the application. All the containers, box and buttons
# are instaciated here. The main window is composed by a HeaderBar, which is called NavigationBar,

	def __init__(self):
		# Start the controller
		ctrl = Control.CController()

		# Program main window.
		Gtk.Window.__init__(self, title="Hello World!")
		# Get screen size and resize the program window to fill the screen.
		screen = self.get_screen()
		self.set_default_size(screen.get_width(), screen.get_height())

		self.add_main_box()
		self.add_navigation_bar()
		self.add_horizontal_box()
		self.add_project_box()
		self.add_notebook(ctrl=ctrl)

		# Buttons for test

		self.button1 = Gtk.Button(label="Click Here")
		self.button1.connect("clicked", ctrl.on_button_clicked)
		self.vert_box.pack_start(self.button1, False, False, 0)

		self.button2 = Gtk.Button(label="Click Here Too")
		self.button2.connect("clicked", ctrl.print_debug)
		self.vert_box.pack_start(self.button2, False, False, 0)

		self.button3 = Gtk.Button(label="Click Here Too")
		self.button3.connect("clicked", self.print_debug)
		self.vert_box.pack_start(self.button3, False, False, 0)

	def print_debug(self, widget):
		print(self.vert_box.props.orientation)

	def add_main_box(self):
		# First Box container in vertical orientation that hold the HeaderBar and the following layout containers
		self.vert_box = Gtk.Box(spacing=6,
		                        homogeneous=False,
		                        orientation='GTK_ORIENTATION_VERTICAL')
		self.add(self.vert_box)

	def add_navigation_bar(self):
		# Add the navigation bar that show the buttons responsible by control the ERA engine.
		self.navbar = Gtk.HeaderBar(title="Header Bar Example")

		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		self.navbar.pack_end(button)

		# A Box container that is set inside the NavigationBar to handle the buttons
		hb_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
		Gtk.StyleContext.add_class(hb_box.get_style_context(), "linked")

		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
		hb_box.add(button)

		button = Gtk.Button()
		button.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
		hb_box.add(button)

		self.navbar.pack_start(hb_box)
		self.vert_box.pack_start(self.navbar, False, False, 0)

	def add_horizontal_box(self):
		# A Box container with horizontal orientation that handle the Notebook container
		self.horizontal_box = Gtk.Box(homogeneous=True,
		                              orientation=Gtk.Orientation.HORIZONTAL)
		self.vert_box.pack_start(self.horizontal_box, True, True, 0)

	def add_project_box(self):
		# Add a Listbox that show the project structure
		listbox = Gtk.ListBox()
		listbox.set_selection_mode(Gtk.SelectionMode.MULTIPLE)
		# allocation = listbox.get_allocation()
		# allocation.height = 200
		# allocation.width = 100
		# listbox.set_allocation(allocation)
		self.horizontal_box.pack_start(listbox, True, True, 0)



		#Add a header to the Listbox
		row = Gtk.ListBoxRow()
		hb = Gtk.HeaderBar(title="Project")
		button = Gtk.Button()
		icon = Gio.ThemedIcon(name="mail-send-receive-symbolic")
		image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
		button.add(image)
		hb.pack_end(button)
		row.add(hb)
		listbox.show_all()

	def add_notebook(self, ctrl):

		self.nb = Gtk.Notebook()
		self.page_environment = Gtk.Overlay()
		graph = ctrl.get_graph()
		graph_widget = gtk_graph_draw.GraphWidgetWithBackImage(graph,
		                                                       pos=graph.vertex_properties["position"],
		                                                       vertex_size=80,
		                                                       vertex_text=graph.vertex_properties["name"],
		                                                       vertex_text_position=-5,
		                                                       vertex_font_size=12,
		                                                       edge_pen_width=graph.edge_properties["contaminationCriteria"],
		                                                       geometry=(1440, 1024),
		                                                       edge_marker_size=30,
		                                                       bg_color=[1, 1, 1, 0],
		                                                       bg_image="terrain.png") #Only .png files are accepted

		self.page_environment.add_overlay(graph_widget)
		# self.page_environment.add(Gtk.Label('Environment simulation page'))
		self.nb.append_page(self.page_environment, Gtk.Label('Environment'))

		self.page_plot = Gtk.Box()
		self.page_plot.set_border_width(10)
		self.page_plot.add(Gtk.Label('A page with an image for a Title.'))
		self.nb.append_page(self.page_plot,
		                    Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU)
		                    )

		self.horizontal_box.add(self.nb)