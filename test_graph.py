# coding=utf-8
from graph_tool.all import *
from random import *

import LoadData
import math
import shapefile

class CEnvironmentGraph():
    """This class instantiate a graph-tool.Graph object and set the vertex and edge properties accordingly
    to the configuration file."""

    def __init__(self, species, connections):

        self.g = Graph()  # Create new graph object
        self.species = species
        self.connections = connections
        self.w_width = 0
        self.w_height = 0
        self.max_vertex = 5000
        self.v_total = 0
        self.pixel_step = 15

        self.names = []
        self.v_pos = []
        self.g.vertex_properties.position = self.g.new_vertex_property("vector<double>")
        self.g.vertex_properties.species = self.g.new_vertex_property("string")
        self.g.vertex_properties.spread_model = self.g.new_vertex_property("vector<string>")
        self.g.vertex_properties.group = self.g.new_vertex_property("vector<string>")
        self.g.vertex_properties.habitat = self.g.new_vertex_property("vector<string>")
        self.g.vertex_properties.state = self.g.new_vertex_property("vector<string>")
        self.g.vertex_properties.state_color = self.g.new_vertex_property("vector<double>")

    def update_dimensions(self, ww, wh, wx, wy):
        # Update the widget dimensions where the graph is being drawn
        self.w_width = ww
        self.w_height = wh
        self.w_pos_x = wx
        self.w_pos_y = wy
        # print("Updated dimensions", ww, wh)
        # print("Widget start position", wx, wy)

    def read_shapes(self, sf):
        self.sf = shapefile.Reader(sf)
        self.x1 = self.sf.bbox[0]
        self.y1 = self.sf.bbox[1]
        self.x2 = self.sf.bbox[2]
        self.y2 = self.sf.bbox[3]
        self.shapes = self.sf.shapes()
        records = self.sf.records()

    def gen_graph(self):
        self.calc_pos()
        self.add_vertices()
        self.add_edges()

    def calc_pos(self):
        """ Set the vertices positions"""
        img_width = self.w_width / 4
        img_height = self.w_height / 3
        width_ratio = float(self.w_width) / float(img_width)
        height_ratio = float(self.w_height) / float(img_height)
        self.scale_xy = min(width_ratio, height_ratio)

        top = int((self.w_height / 2) - (img_height * self.scale_xy / 2))
        left = int((self.w_width / 2) - (img_width * self.scale_xy / 2))
        offset = (left + self.w_pos_y, top + self.w_pos_y)

        v_count = 0
        for i in range(len(self.shapes)):
            print(self.shapes[i].parts)
            progress = int(100 * i / len(self.shapes))
            print("Progress: " + str(progress) + "%")
        # for i in range(0, 1):
            if v_count < self.max_vertex:
                coords = self.shapes[i].points
                x_max, x_min, y_max, y_min = coords[0][0], coords[0][0], coords[0][1], coords[0][1]
                # Find maximum and minimum value of shapes coordinates
                for j in range(len(coords)):
                    if coords[j][0] > x_max:
                        x_max = coords[j][0]
                    if coords[j][0] < x_min:
                        x_min = coords[j][0]

                    if coords[j][1] > y_max:
                        y_max = coords[j][1]
                    if coords[j][1] < y_min:
                        y_min = coords[j][1]

                # Normalize maximum and minimum values of shape coordinates and convert to widget dimensions
                x_max_norm = (x_max - self.x1) / (self.x2 - self.x1)
                y_max_norm = (y_max - self.y1) / (self.y2 - self.y1)
                x_min_norm = (x_min - self.x1) / (self.x2 - self.x1)
                y_min_norm = (y_min - self.y1) / (self.y2 - self.y1)

                x_max = int((x_max_norm * self.w_width) / 4)
                x_min = int((x_min_norm * self.w_width) / 4)
                y_min = int((self.w_height - (y_max_norm * self.w_height)) / 3)
                y_max = int((self.w_height - (y_min_norm * self.w_height)) / 3)

                # Set coordinates where the vertices should be drawn
                for column in range(y_min, y_max, self.pixel_step):
                    if v_count < self.max_vertex:
                        for row in range(x_min, x_max, self.pixel_step):
                            # print(self.is_inside(coords, len(coords) - 1, list([column, row])))
                            if self.is_inside(coords, len(coords) - 1, list([column, row]), self.shapes[i]) == 1:
                                if v_count < self.max_vertex and [column, row] not in self.v_pos:
                                    self.v_pos.append([(column * self.scale_xy) + offset[0],
                                                       (row * self.scale_xy) + offset[1]])
                                    v_count += 1
                                else:
                                    break
                            # if x_min <= column <= x_max and y_min <= row <= y_max:
                                # if v_count < self.max_vertex and [column, row] not in self.v_pos:
                                #     self.v_pos.append([(column * self.scale_xy) + offset[0],
                                #                        (row * self.scale_xy) + offset[1]])
                                #     # self.v_pos.append([column, row])
                                #     # print("Coordinates:", column, row)
                                #     v_count += 1
                                # else:
                                #     break
                    else:
                        break
            else:
                break
        print("Vertices total:", v_count)
        if v_count == 0:
            self.v_total = v_count
        else:
            self.v_total = v_count - 1


    @staticmethod
    def on_segment(p, r, q):
        """
        Given three collinear points p, q, r, the function checks if point q lies on line segment 'pr'
        :param p: List with x and y coordinates of first point of the segment 'pr'
        :type p: list
        :param r: List with x and y coordinates of second point of the segment 'pr'
        :type r: list
        :param q: List with x and y coordinates of point to verify collinearity
        :type q: list
        :return: Return True if the point q is collinear to segment 'pr', False otherwise.
        :rtype: bool
        """
        if min(p[0], r[0]) <= q[0] <= max(p[0], r[0]) and \
                min(p[1], r[1]) <= q[1] <= max(p[1], r[1]):
            return True
        else:
            return False

    @staticmethod
    def orientation(p, q, r):
        """
        To find orientation of ordered triplet (p, q, r).
        The function returns following values
        0 --> p, q and r are collinear
        1 --> Clockwise
        2 --> Counterclockwise
        :param p: List with x and y coordinates of first point of the segment 'pq'
        :type p: list
        :param q: List with x and y coordinates of second point of the segment 'pq'
        :type q: list
        :param r: List with x and y coordinates of point to verify the orientation
        :type r: list
        :return: Return a integer correspondent to the orientation of segment 'pq' related to point r
        :rtype: int
        """
        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/
        # for details of below formula.
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0:
            return 0  # collinear

        elif val > 0:
            return 1  # clockwise
        else:
            return 2  # counterclockwise

    def do_intersect(self, p1, q1, p2, q2):
        """
        This function verify if line segment 'p1q1' and 'p2q2' intersect each other.
        :param p1: List with x and y coordinates of first point of the segment 'p1q1'
        :type p1: list
        :param q1: List with x and y coordinates of second point of the segment 'p1q1'
        :type q1: list
        :param p2: List with x and y coordinates of first point of the segment 'p2q2'
        :type p2: list
        :param q2: List with x and y coordinates of second point of the segment 'p2q2'
        :type q2: list
        :return: Return True if segment 'p1q1' intersects segment 'p2q2'
        :rtype: bool
        """
        # Find the four orientations needed for general and special cases
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        # General case
        if o1 != o2 and o3 != o4:
            return True

        # Special Cases
        # p1, q1 and p2 are collinear and p2 lies on segment p1q1
        if o1 == 0 and self.on_segment(p1, q1, p2):
            return True

        # p1, q1 and p2 are collinear and q2 lies on segment p1q1
        if o2 == 0 and self.on_segment(p1, q1, q2):
            return True

        # p2, q2 and p1 are collinear and p1 lies on segment p2q2
        if o3 == 0 and self.on_segment(p2, q2, p1):
            return True

        # p2, q2 and q1 are collinear and q1 lies on segment p2q2
        if o4 == 0 and self.on_segment(p2, q2, q1):
            return True

        return False  # Doesn't fall in any of the above cases

    def is_inside(self, polygon, n, p, shape):
        """
        Returns true if the point p lies inside the polygon[] with n vertices
        :param polygon: List of x and y coordinates that compose the polygon
        :type polygon: list
        :param n: Polygon numberr of vertices
        :type n: int
        :param p: Point to verify if is inside of polygon
        :type p: list
        :param shape: Object with information about the polygon to check if the point is within
        :type shape: object
        :return: Return True if the number of intersections is odd, which means the point is inside the polygon,
        False otherwise
        :rtype: bool
        """
        # There must be at least 3 vertices in polygon[]
        if n < 3:
            return False

        # Create a point for line segment from p to infinite
        extreme = [self.w_width, p[1]]

        # Count intersections of the above line with sides of polygon
        count = 0
        i = 0
        # print(shape.parts)
        while True:
            next = (i+1) % n
            if next in shape.parts and next != 0:
                next += 1
                i += 1
            p1 = list(polygon[i])
            q1 = list(polygon[next])

            # Normalize values of shape coordinates and convert to widget dimensions
            p1[0] = (p1[0] - self.x1) / (self.x2 - self.x1)
            p1[1] = (p1[1] - self.y1) / (self.y2 - self.y1)
            q1[0] = (q1[0] - self.x1) / (self.x2 - self.x1)
            q1[1] = (q1[1] - self.y1) / (self.y2 - self.y1)

            p1[0] = (p1[0] * self.w_width) / 4
            p1[1] = (self.w_height - (p1[1] * self.w_height)) / 3
            q1[0] = (q1[0] * self.w_width) / 4
            q1[1] = (self.w_height - (q1[1] * self.w_height)) / 3

            # Check if the line segment from 'p' to 'extreme' intersects
            # with the line segment from 'polygon[i]' to 'polygon[next]'
            if self.do_intersect(p1, q1, p, extreme):
                # If the point 'p' is collinear with line segment 'i-next',
                # then check if it lies on segment. If it lies, return true,
                # otherwise false
                if self.orientation(p1, q1, p) == 0:
                    return self.on_segment(p1, q1, p)
                count += 1
            i = next
            if i == 0:
                break

        # Return true if count is odd, false otherwise
        return count & 1  # Same as (count%2 == 1)

    def add_vertices(self):
        """
        Create graph vertices and species properties for each vertex.
        :return: None
        :rtype: None
        """
        self.g.add_vertex(self.v_total)
        vprop_pos = self.g.new_vertex_property("vector<double>")

        # Read the species properties from the JSON file and insert into vertex properties
        for v in self.g.vertices():
            n = randint(0, len(self.species) - 1)
            s = self.species[n]
            self.g.vertex_properties.species[v] = s["species"]
            self.g.vertex_properties.spread_model[v] = s["spread_model"]
            self.g.vertex_properties.group[v] = s["group"]
            self.g.vertex_properties.habitat[v] = s["habitat"]
            self.g.vertex_properties.state[v] = s["state"]
            # Color for susceptible (S) state
            self.g.vertex_properties.state_color[v] = (186 / 255, 172 / 255, 18 / 255, 0.8)

        for count in range(0, self.v_total, 1):
            vprop_pos[count] = self.v_pos[count]

        self.g.vertex_properties.position = vprop_pos

    def add_edges(self):
        # Create edges between graph vertices, respecting the species connections and the maximum distance
        # between vertices.
        count = 0
        total = 0
        dist_max = self.pixel_step * self.scale_xy  # Maximum acceptable distance between two vertices to create an edge.
        for s in self.connections:
            vertex_list = []
            pos_list = []
            # Create a vertex list identifying the vertex that can be connected to a specific specie, respecting the
            # relations described in connections.json.
            for v in self.g.get_vertices():
                if self.g.vertex_properties.species[v] == s:
                    vertex_list.append(v)
                    pos_list.append(self.g.vertex_properties.position[v])

            for v2 in self.g.get_vertices():
                # Create edges between vertices identified in the last step, whereas the maximum distance (in pixels)
                # between them can't be greater then the value of dist_max
                if v2 not in vertex_list and self.g.vertex_properties.species[v2] in self.connections[s]:
                    for v1 in vertex_list:
                        x1, y1 = self.g.vertex_properties.position[v1]
                        x2, y2 = self.g.vertex_properties.position[v2]
                        # print(x1, y1, x2, y2)
                        # print(self.g.edge(v1, v2), self.g.edge(v2, v1))
                        if math.fabs(x1 - x2) <= dist_max and math.fabs(y1 - y2) <= dist_max and \
                            self.g.edge(v1, v2) is None and self.g.edge(v2, v1) is None:
                            self.g.add_edge(v1, v2)
                            count += 1
            total += count
            print(s, count)
            count = 0
        print("Total:", total)

    def get_groups(self):
        available_groups = []
        for s in self.species:
            for group in s["group"]:
                if group not in available_groups:
                    available_groups.append(group)
        return available_groups

    def get_graph(self):
        """Return the graph object"""
        return self.g
