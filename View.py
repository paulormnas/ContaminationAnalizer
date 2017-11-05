# coding=utf-8
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, Gdk
from graph_tool.all import *

import Control, gtk_graph_draw

class CMainWindow(Gtk.Window):
# This class is used to create the main window of the application. All the containers, box and buttons
# are instaciated here. The main window is composed by a HeaderBar, which is called NavigationBar,

	def __init__(self):
		# Start the controller
		ctrl = Control.CController()
		self.graph = ctrl.get_graph()

		# Program main window.
		Gtk.Window.__init__(self, title="Hello World!")
		# Get screen size and resize the program window to fill the screen.
		screen = self.get_screen()
		self.set_default_size(screen.get_width(), screen.get_height())
		self.connect("key-press-event", self.key_press_event)

		self.add_main_box()
		self.add_navigation_bar()
		self.add_horizontal_pane()
		self.add_project_view()
		self.add_notebook()

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
		self.vert_box = Gtk.Box(homogeneous=False,
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

	def add_horizontal_pane(self):
		# A Paned container with horizontal orientation that handle the notebook and project view
		self.horizontal_pane = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
		self.vert_box.pack_start(self.horizontal_pane, True, True, 0)

	def add_project_view(self):
		# Create a porject view composed by a header and a ListBox that show the structure of itens present
		# in the project
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
		allocation = Gdk.Rectangle(x=0,
		                           y=0,
		                           width=self.project_view_box.get_allocated_width(),
		                           heihgt=15)
		hb.size_allocate(allocation)
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

		for name in self.graph.vertex_properties["name"]:
			exp = Gtk.Expander()
			exp.set_label_widget(self.project_view_item_label(label=name,
			                                                  icon="vertex"))
			row = Gtk.ListBoxRow()
			row.add(exp)
			listbox.add(row)
		listbox.show_all()

	def project_view_item_label(self, label, icon):
		# This function is used to construct the label of the items in the project view
		item_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
		                  homogeneous=False,
		                  spacing=6)
		item_label = Gtk.Label()
		item_label.set_text(label)

		if icon == "vertex":
			item_icon = Gtk.Image.new_from_file("icons/vertex.png")
		else:
			item_icon = None

		item_box.add(item_icon)
		item_box.pack_start(item_label, False, False, 0)
		return item_box

	def add_notebook(self):

		self.nb = Gtk.Notebook()

		self.page_environment = Gtk.Overlay()

		self.graph_widget = gtk_graph_draw.GraphWidgetWithBackImage(self.graph,
		                                                       pos=self.graph.vertex_properties["position"],
		                                                       vertex_size=80,
		                                                       vertex_text=self.graph.vertex_properties["name"],
		                                                       vertex_text_position=-5,
		                                                       vertex_font_size=12,
		                                                       edge_pen_width=self.graph.edge_properties["contaminationCriteria"],
		                                                       geometry=(1440, 1024),
		                                                       edge_marker_size=30,
		                                                       bg_color=[1, 1, 1, 0],
		                                                       bg_image="terrain.png") #Only .png files are accepted

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


	def key_press_event(self, widget, event):
		# Handle key press.

		# If the page_environment is displayed than handle the event key inside graph_widget
		if self.nb.get_current_page() == 0:
			self.graph_widget.key_press_event(self.graph_widget, event=event)
