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
        self.sf = "shapefile/clipabaetetubasolo.shp"
        self.ctrl = Control.CController()
        self.ctrl.set_shapefile(self.sf)
        self.graph = self.ctrl.get_graph()
        self.graph_widget = None
        self.is_running = False  # Attribute to control thread activity
        
        # Program main window.
        Gtk.Window.__init__(self, title="CSA") # CSA - Contamination Spreading Analyser
        # Get screen size and resize the program window to fill the screen.
        self.set_icon_from_file("icons/vertex.png")
        self.screen = self.get_screen()
        self.set_default_size(self.screen.get_width(), self.screen.get_height())

        # Events handled
        self.connect("key-press-event", self.key_press_event)

        # Create other elements of the interface
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
        button.set_image(Gtk.Image.new_from_file("icons/connections.png"))
        button.connect("clicked", self.update_connections)
        config_box.add(button)

        button = Gtk.Button()
        button.set_image(Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU))
        button.connect("clicked", self.generate_graph)
        config_box.add(button)

        # A box container that is set inside the NavigationBar to handle the buttons that controls the simulator
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

        # Box to handle the scale and it's icon
        scl_box = Gtk.Box(orientation='GTK_ORIENTATION_HORIZONTAL', homogeneous=False)
        scl_box.pack_start(scl_img, False, False, 0)
        scl_box.pack_start(self.scale, True, True, 0)

        # Button that allow change the state of random species to infected
        infect_btn = Gtk.Button(label='Infect')
        infect_btn.connect("clicked", self.infect)

        # Box to handle the scale and it's icon
        infect_box = Gtk.Box(orientation='GTK_ORIENTATION_HORIZONTAL', homogeneous=False)
        infect_box.pack_start(infect_btn, False, False, 0)

        # Combobox to select the group to be observed on the map. For example, by selecting group TcI the user can
        # see the state of all species that can be infected by TcI.
        self.group_combo = Gtk.ComboBoxText()
        self.group_combo.connect("changed", self.on_group_combo_changed)
        self.update_combobox()

        # Box to handle the button's box and scale's box and add space between then
        hb_box_sim = Gtk.Box(orientation='GTK_ORIENTATION_HORIZONTAL', homogeneous=True, spacing=20)
        hb_box_sim.pack_start(btn_box, True, False, 0)
        hb_box_sim.pack_start(scl_box, True, True, 0)
        hb_box_sim.pack_start(infect_box, True, True, 0)
        hb_box_sim.pack_start(self.group_combo, True, True, 0)

        # Box to handle the configuration buttons and separate then from the buttons that controls the simulation
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
        """Create a project view composed by a header and a ListBox that show the structure of items present
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

        # A Box container that is set inside the NavigationBar to handle decorations
        project_hb_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(project_hb_box.get_style_context(), "linked")
        icon = Gtk.Image.new_from_file("icons/connections.png")
        project_hb_box.add(icon)
        label = Gtk.Label(" Project")
        project_hb_box.add(label)
        hb.pack_start(project_hb_box, False, False, 0)

        # Add the ListBox with project items information
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.project_view_box.pack_end(self.listbox, True, True, 6)

        # Expander for vertex properties
        exp = Gtk.Expander()
        exp.set_label_widget(self.project_view_expander_label(label="Selected Vertex", icon="vertex"))
        row = Gtk.ListBoxRow()
        row.add(exp)
        self.listbox.add(row)
        props = {"Species": "", "Spread Model": "", "Tc Group": "", "Habitat": ""}
        exp.add(self.project_view_expander_description(dct=props))

        # Expander for vertex connections
        exp = Gtk.Expander()
        exp.set_label_widget(self.project_view_expander_label(label="Connections", icon="connections"))
        row = Gtk.ListBoxRow()
        row.add(exp)
        self.listbox.add(row)
        self.listbox.show_all()

    @staticmethod
    def project_view_expander_label(label=None, icon=None):
        """This function is used to construct the label of the items in the project view"""
        vbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                       homogeneous=False,
                       spacing=0)

        if icon is not None:
            item_icon = Gtk.Image.new_from_file("icons/" + icon + ".png")
            vbox.add(item_icon)
        item_label = Gtk.Label()
        item_label.set_text(label)
        vbox.pack_end(item_label, False, False, 6)
        return vbox

    @staticmethod
    def project_view_expander_description(dct=None):
        """This function is used to construct the descriptions of the items in the project view with data
        of the vertex selected by the user"""
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                       homogeneous=False,
                       spacing=6)
        spc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                       homogeneous=False,
                       spacing=4)
        exp_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                       homogeneous=False,
                       spacing=4)
        hbox.pack_start(spc_box, False, False, 6)
        hbox.pack_start(exp_box, False, False, 6)

        for k in dct.keys():
            exp_description = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                                      homogeneous=False,
                                      spacing=6)
            description_spc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL,
                                          homogeneous=False,
                                          spacing=6)
            exp_description.pack_start(description_spc_box, False, False, 6)
            if isinstance(dct[k], int):
                item_description = Gtk.Label()
                item_description.set_markup(k + ":\t" + """<span foreground="blue">""" + str(dct[k]) + "</span>")
                exp_description.pack_start(item_description, False, False, 6)
                exp_box.add(exp_description)
            elif isinstance(dct[k], str):
                exp = Gtk.Expander()
                exp.set_label_widget(Gtk.Label(k))
                item_description = Gtk.Label()
                item_description.set_markup("""<span foreground="blue">""" + dct[k] + "</span>")
                exp_description.pack_start(item_description, False, False, 6)
                exp.add(exp_description)
                exp_box.add(exp)
        return hbox

    def add_notebook(self):
        self.nb = Gtk.Notebook()
        self.page_environment = Gtk.Overlay()
        self.graph_widget = gtk_graph_draw.GraphWidgetWithBackImage(self.graph,
                                                                    pos=self.graph.vertex_properties["position"],
                                                                    vertex_size=20,
                                                                    # vertex_text=self.graph.vertex_properties.species,
                                                                    vertex_text_position=-5,
                                                                    vertex_font_size=12,
                                                                    vertex_fill_color=self.graph.vertex_properties.state_color,
                                                                    fit_view=False,
                                                                    # edge_pen_width=self.graph.edge_properties["contaminationCriteria"],
                                                                    edge_marker_size=10,
                                                                    bg_color=[1, 1, 1, 0],
                                                                    bg_image=self.sf    #Only shapefiles are accepted
                                                                    )
        self.graph_widget.connect("size_allocate", self.size_allocate)
        self.graph_widget.connect("button-release-event", self.button_release_event)
        self.page_environment.add_overlay(self.graph_widget)
        # self.page_environment.set_overlay_pass_through(self.graph_widget, True)
        # self.page_environment.add(Gtk.Label('Environment simulation page'))
        self.nb.append_page(self.page_environment, Gtk.Label('Environment'))

        self.page_plot = Gtk.Box()
        self.page_plot.set_border_width(10)
        self.page_plot.add(Gtk.Label('A page with an image for a Title.'))
        self.nb.append_page(self.page_plot,
                            Gtk.Image.new_from_icon_name("help-about", Gtk.IconSize.MENU))
        self.horizontal_pane.add2(self.nb)

    def add_statusbar(self):
        """Add a status bar on the bottom of the window."""
        self.sb = Gtk.Statusbar()
        self.context_id = self.sb.get_context_id("__iteration__")
        self.vert_box.pack_end(self.sb, False, False, 0)

    def size_allocate(self, da, allocation):
        """Update the graph widget dimensions and send to EnvironmentGraph class"""
        self.graph_widget_width = allocation.width
        self.graph_widget_height = allocation.height
        self.widget_pos_x, self.widget_pos_y = Gtk.Widget.translate_coordinates(self.graph_widget,
                                                                                Gtk.Widget.get_toplevel(self),
                                                                                0,
                                                                                0)
        self.ctrl.update_widget_dim(self.graph_widget_width,
                                    self.graph_widget_height,
                                    self.widget_pos_x,
                                    self.widget_pos_y)

    def generate_graph(self, widget):
        t = threading.Thread(target=self.thread_gen_graph)
        t.start()

    def thread_gen_graph(self):
        self.ctrl.gen_graph()
        self.redraw()

    def update_combobox(self):
        """Add items to group combobox on toolbar of the MainView"""
        groups = self.ctrl.get_available_groups()
        for item in groups:
            self.group_combo.append_text(item)
        self.group_combo.set_active(0)

    def on_group_combo_changed(self, cb):
        self.ctrl.update_color_state(cb.get_active_text())
        if self.graph_widget is not None:
            self.redraw()

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
            self.graph = self.ctrl.step_backward(graph=self.graph,
                                                 group_observed=self.group_combo.get_active_text())
            self.redraw()

    def step_forward(self, widget):
        """Execute one step forward in SER simulation"""
        if not self.is_running:
            self.graph = self.ctrl.step_forward(graph=self.graph,
                                                group_observed=self.group_combo.get_active_text())
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
            self.graph = self.ctrl.step_forward(graph=self.graph,
                                                group_observed=self.group_combo.get_active_text())
            GObject.idle_add(self.redraw)
            time.sleep(3 / self.scale.get_value())

    def reset(self, widget):
        """Reset the SER simulation"""
        if not self.is_running:
            self.graph = self.ctrl.reset(graph=self.graph,
                                         group_observed=self.group_combo.get_active_text())
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

    def infect(self, widget):
        """
        Handle the click event on a button to random infect a vertex on the drawn graph
        :param widget: A widget that call a click event
        :type widget: Gtk.Widget
        :return: None
        :rtype: None
        """
        self.ctrl.random_infect_specie(graph=self.graph,
                                       group=self.group_combo.get_active_text())
        self.graph_widget.regenerate_surface(reset=True)
        self.graph_widget.queue_draw()

    def button_release_event(self, widget, event):
        """ Callback function that handle the mouse button release when the user select a graph's vertex"""
        v = self.graph_widget.get_selected_vertex()
        selected_vertex_props = {}  # Dictionary with properties of the vertex selected by the user
        if isinstance(v, graph_tool.Vertex):
            selected_vertex_props["species"] = self.graph.vertex_properties.species[v]
            selected_vertex_props["spread_model"] = self.graph.vertex_properties.spread_model[v]
            selected_vertex_props["group"] = self.graph.vertex_properties.group[v]
            selected_vertex_props["habitat"] = self.graph.vertex_properties.habitat[v]
            selected_vertex_props["state"] = self.graph.vertex_properties.state[v]
            neighbor_dct = {}
            for n in self.graph.get_in_neighbors(v):
                self.add_especies_to_dct(dct=neighbor_dct, v=n)
            for n in self.graph.get_out_neighbors(v):
                self.add_especies_to_dct(dct=neighbor_dct, v=n)
            selected_vertex_props["neighbors"] = neighbor_dct
            self.update_listbox(props=selected_vertex_props)

    def add_especies_to_dct(self, dct, v):
        species = self.graph.vertex_properties.species[v]
        if species in dct.keys():
            dct[species] = dct[species] + 1
        else:
            dct[species] = 1

    def update_listbox(self, props):
        """
        Update the Listbox of project view when the user select a vertex.
        :param props: Dictionary that contains the properties of graph's vertex
        :type props: dict
        :return: None
        :rtype: None
        """
        for child in self.listbox.get_children():
            self.listbox.remove(child)

        exp = Gtk.Expander()
        exp.set_label_widget(self.project_view_expander_label(label="Selected Vertex", icon="vertex"))
        row = Gtk.ListBoxRow()
        row.add(exp)
        self.listbox.add(row)

        dct_to_print = {"Species": props["species"],
                        "Spread Model": self.string_construct(lst=list(props["spread_model"])),
                        "Tc Group": self.string_construct(lst=list(props["group"])),
                        "Habitat": self.string_construct(lst=list(props["habitat"]))}
        exp.add(self.project_view_expander_description(dct=dct_to_print))

        exp = Gtk.Expander()
        exp.set_label_widget(self.project_view_expander_label(label="Connections", icon="connections"))
        exp.add(self.project_view_expander_description(dct=props["neighbors"]))
        row = Gtk.ListBoxRow()
        row.add(exp)
        self.listbox.add(row)
        self.listbox.show_all()

    @staticmethod
    def string_construct(lst):
        """
        Build a string with the information passed through the list
        :param lst: List of string with data to be concatenated
        :type lst: list
        :return: String with the adapted information to be shown as a vertical list
        :rtype: str
        """
        final_str = ""
        for obj in lst:
            if lst.index(obj) == (len(lst) - 1):
                final_str = final_str + str(obj)
            else:
                final_str = final_str + str(obj) + "\r"
        return final_str
