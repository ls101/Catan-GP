import random
from board_specs import *
from board_components import Terrain, Edge, Intersection, ports


class Board:
    def __init__(self):
        # Initialize a list for each attribute type.
        self.edges = self.initialize_edges()
        self.intersections = self.initialize_intersections()
        self.terrains = self.initialize_terrains()
        # Assign the correct attributes for each attribute.
        self.a_edge()
        self.a_intersection()
        self.a_terrain()

    def __str__(self):
        # A message, of how the board is displayed.
        s = '\nThe board is arranged as follows:\n'
        s += '   /\\ /\\ /\\ \n'
        s += '  |01|02|03| \n'
        s += '   \\/ \\/ \\/ \n'
        s += '  /\\ /\\ /\\ /\\ \n'
        s += ' |04|05|06|07| \n'
        s += '  \\/ \\/ \\/ \\/ \n'
        s += ' /\\ /\\ /\\ /\\ /\\ \n'
        s += '|08|09|10|11|12| \n'
        s += ' \\/ \\/ \\/ \\/ \\/ \n'
        s += '  /\\ /\\ /\\ /\\ \n'
        s += ' |13|14|15|16| \n'
        s += '  \\/ \\/ \\/ \\/ \n'
        s += '   /\\ /\\ /\\ \n'
        s += '  |17|18|19| \n'
        s += '   \\/ \\/ \\/ \n'
        # Display each terrains; the identifying numbers correspond to
        # the above diagram.
        s += 'Following is the content of each terrain:\n\n'
        for item in range(1, len(self.terrains)):
            s += str(self.terrains[item])
        return s

    # The following methods will initialize all objects with default
    # arguments; their attribute objects will be reassigned later.  This
    # is because the objects refer each other as attributes, and they
    # must exist before being assigned.  The objects will be stored in a
    # dictionary, with reference numbers as keys.  Since some edges and
    # intersections border the ocean, a key #0 is initialized with a
    # string (instead of an object.)
    def initialize_edges(self):
        edges = {0: 'ocean'}
        for x in range(1, 73):
            edges[x] = Edge(x)
        return edges

    def initialize_intersections(self):
        intersections = {0: 'ocean'}
        for x in range(1, 55):
            intersections[x] = Intersection(x)
        return intersections

    def initialize_terrains(self):
        terrains = {0: 'ocean'}
        for x in range(1, 20):
            terrains[x] = Terrain(x, x, 'Dessert')
        return terrains

    # The following methods will assign the correct attributes for each
    # object.  It does not matter if the object that's assigned already
    # has it's own attributes referred to properly, or if it will be
    # assigned later.  The pointers remain unchanged, and all objects
    # will have their proper attributes.  This circular relationship is
    # interesting.  An object's attribute's attribute can be the initial
    # object.
    def a_edge(self) -> None:
        for item in edges_specs:
            # index = item[0]
            # Pass the objects, as tuples, to reassign the attributes of the
            # object.
            self.edges[item[0]].intersections = (item[1])
            self.edges[item[0]].terrain = (item[2])

    def a_intersection(self) -> None:
        for item in intersections_specs:
            # Pass the objects, as tuples, to reassign the attributes of the
            # object.
            self.intersections[item[0]].edges = (item[1])
            # If that item contains a port, assign it here.
            if len(item) == 3:
                self.intersections[item[0]].ports = item[2]

    # The attribute for the terrains.
    landscapes = [
        'Hills',
        'Hills',
        'Hills',
        'Forest',
        'Forest',
        'Forest',
        'Forest',
        'Mountains',
        'Mountains',
        'Mountains',
        'Fields',
        'Fields',
        'Fields',
        'Fields',
        'Pasture',
        'Pasture',
        'Pasture',
        'Pasture',
        'Dessert'
    ]
    resource_nums = [
        2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12
        ]
    # Shuffle the lists, so that each board is unique.
    random.shuffle(landscapes)
    random.shuffle(resource_nums)

    def a_terrain(self) -> None:
        for item in terrains_specs:

            # Pass the objects, as tuples, to reassign the attributes of the
            # object.
            self.terrains[item[0]].edges = item[1]
            self.terrains[item[0]].intersections = item[2]

            # Assign the last landscape and resource number.  (The lists
            # were shuffled, so it's random.)  The dessert doesn't have a
            # resource number, and it has the robber.
            landscape = self.landscapes.pop()
            self.terrains[item[0]].landscape = landscape
            self.terrains[item[0]].resource = Terrain.resources[landscape]
            if landscape == 'Dessert':
                self.terrains[item[0]].has_robber = True
                self.terrains[item[0]].resource_num = None
            else:
                self.terrains[item[0]].resource_num = self.resource_nums.pop()



# Create and display the board object.
def main():
    b = Board()
    print(b)


if __name__ == '__main__':
    main()
