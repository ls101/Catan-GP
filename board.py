import numpy as np
import random
from board_specs import *
from board_components import Terrain, Edge, Intersection


# List of resources available to be distributed on the board
RESOURCE_NAMES = ["desert", "brick", "ore", "hay", "wood", "sheep"]
# Create a dictionary of each resource and a corresponding number id
res_dict = dict(zip(RESOURCE_NAMES, np.arange(0, len(RESOURCE_NAMES))))
# List of available ports that can be distributed around the board
PORTS_NAMES = ["3:1", "2brick:1", "2ore:1", "2hay:1", "2wood:1", "2sheep:1"]
# Create a dictionary of each port and a corresponding number id
port_dict = dict(zip(PORTS_NAMES, np.arange(0, len(PORTS_NAMES))))

class Board:
    def __init__(self):
        """initiates CatanBoard()/self according to catan rules:
        Do not forget to ensure 6 and 8 are not next to each other: no 6-6 no 6-8 no 8-8
        """
        # Array of each resource id number repeated the amount of times that the resource is available on the board
        # This will be used to distribute the resources into slots on the board
        self.board_resources = np.array(
            [res_dict["desert"]] + [res_dict["brick"]] * 3 + [res_dict["ore"]] * 3 + [res_dict["hay"]] * 4 + [
                res_dict["wood"]] * 4 + [res_dict["sheep"]] * 4)
        # Shuffle the resource array for randomized distribution
        np.random.shuffle(self.board_resources)
        # number associated with the desert and 0 can not actually be rolled
        self.roll_numbers = np.array([0, 2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12])
        # shuffle number options
        np.random.shuffle(self.roll_numbers)
        # Array of the port ids, amount of times each port is available -
        self.ports = np.array(
            [port_dict["3:1"]] * 4 + [port_dict["2brick:1"]] + [port_dict["2ore:1"]] + [port_dict["2hay:1"]] +
            [port_dict["2wood:1"]] + [port_dict["2sheep:1"]])
        # shuffle the ports for randomized distribution
        np.random.shuffle(self.ports)
        # Zero_tile_nr will represent where the 0 number exists
        zero_tile_nr = np.where(self.roll_numbers == 0)
        # Desert_tile_nr will represent where the desert resource exists
        desert_tile_nr = np.where(self.board_resources == res_dict["desert"])
        # Robber will keep track of where the robber is and it starts in the desert
        self.robber = desert_tile_nr
        # as the desert tile and replace whatever was already in the desert tile into the empty zero tile
        self.roll_numbers[zero_tile_nr], self.roll_numbers[desert_tile_nr] =\
            (self.roll_numbers[desert_tile_nr], self.roll_numbers[zero_tile_nr])
        
        # The following code create the board objects: terrains, edges, intersections.
        
        # Initialize a list for each attribute type.
        self.edges = self.initialize_edges()
        self.intersections = self.initialize_intersections()
        self.terrains = self.initialize_terrains()
        # Assign the correct attributes for each attribute.
        # self.assign_intersection()
        self.assign_specs()
        self.assign_ports()

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
    # dictionary, with reference numbers as keys.
    def initialize_edges(self):
        edges = {}
        for x in range(1, 73):
            edges[x] = Edge(x)
        return edges

    def initialize_intersections(self):
        intersections = {}
        for x in range(1, 55):
            intersections[x] = Intersection(x)
        return intersections

    def initialize_terrains(self):
        terrains = {}
        for x in range(1, 20):
            terrains[x] = Terrain(x, x, 0)
        return terrains

    # The following methods will assign the correct attributes for each
    # object.  It does not matter if the object that's assigned already
    # has it's own attributes referred to properly, or if it will be
    # assigned later.  The pointers remain unchanged, and all objects
    # will have their proper attributes.  This circular relationship is
    # interesting.  An object's attribute's attribute can be the initial
    # object.

    # def assign_intersection(self) -> None:
    #     for item in intersections_specs:
    #         # If that item contains a port, assign it here.
    #         if len(item) == 3:
    #             self.intersections[item[0]].ports = self.ports[item[2]]

    
    def assign_specs(self) -> None:
        for item in terrains_specs:
            # Identify the correct objects from the initialized lists, based
            # on the values of the tuple parameters.
            local_egdes = []
            for subitem in item[1]:
                local_egdes.append(self.edges[subitem])
                self.edges[subitem].terrains.append(self.terrains[item[0]])
            local_intersections = []
            for subitem in item[2]:
                local_intersections.append(self.intersections[subitem])
                self.intersections[subitem].terrains.append(self.terrains[item[0]])

            # Pass the objects, as tuples, to reassign the attributes of the
            # object.
            self.terrains[item[0]].edges = (tuple(local_egdes))
            self.terrains[item[0]].intersections = (tuple(local_intersections))

            # Assign the last landscape and resource number.  (The lists
            # were shuffled, so it's random.)
            self.terrains[item[0]].resource = self.board_resources[item[0]-1]
            self.terrains[item[0]].resource_num = self.roll_numbers[item[0]-1]

    def assign_ports(self):
        for port_list in range(len(ports_specs)):
            print(port_list)
            for intersection in ports_specs[port_list]:
                self.intersections[intersection].port = self.ports[port_list]


# Create and display the board object.
def main():
    b = Board()
    print(b)
    # print(b.edges[1].terrains)
    # for item in b.edges[29].get_neighbors():
    #     print(item.identifier, end=', ')
    # # for key, val in b.edges.items():
    # #     item = val.get_neighbors()
    # #     print(item)

    # for key, val in b.edges.items():
        # print(str(key) + ': ' + str(type(val)))


if __name__ == '__main__':
    main()
