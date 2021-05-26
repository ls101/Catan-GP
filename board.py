import numpy as np
import random
from board_specs import *
from board_components import *
import constants
import player


# List of resources available to be distributed on the board
RESOURCE_NAMES = constants.RESOURCE_NAMES
# Create a dictionary of each resource and a corresponding number id
res_dict = dict(zip(RESOURCE_NAMES, np.arange(0, len(RESOURCE_NAMES))))
# List of available ports that can be distributed around the board
PORTS_NAMES = constants.PORTS_NAMES
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
        # Robber will be an integer.
        # Numpy returns a tuple of which the first is a list with the index.
        # We'll extract it, and add 1 since terrain keys start at 1, not 0.
        self.robber = desert_tile_nr[0][0] +1
        # as the desert tile and replace whatever was already in the desert tile into the empty zero tile
        self.roll_numbers[zero_tile_nr], self.roll_numbers[desert_tile_nr] =\
            (self.roll_numbers[desert_tile_nr], self.roll_numbers[zero_tile_nr])
        
        # The following code create the board objects: terrains, edges, intersections.
        
        # Initialize a list for each attribute type.
        self.edges = self.initialize_edges()
        self.intersections = self.initialize_intersections()
        self.terrains = self.initialize_terrains()
        # Assign the correct attributes for each attribute.
        self.assign_specs()
        self.dev_cards=np.array('knight'*14,'victory point'*5,'road building'*2,'year of plenty'*2,'monopoly'*2)
        self.dev_cards=random.shuffle(dev_cards)

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
        for item in self.terrains:
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
            edges[x] = Edge(x, intersections=[], terrains=[])
        return edges

    def initialize_intersections(self):
        intersections = {}
        for x in range(1, 55):
            intersections[x] = Intersection(x, edges=[], terrains=[])
        return intersections

    def initialize_terrains(self):
        terrains = {}
        for x in range(1, 20):
            terrains[x] = Terrain(x, x, 0)
        return terrains

    # The following method will assign the correct attributes for each
    # object.  It does not matter if the object that's assigned already
    # has it's own attributes referred to properly, or if it will be
    # assigned later.  The pointers remain unchanged, and all objects
    # will have their proper attributes.  This circular relationship is
    # interesting.  An object's attribute's attribute can be the initial
    # object.  
    def assign_specs(self) -> None:
        # First, it loops through the list of terrains from the board_specs
        # file.  The first item is the key/identifier.  Then there are two
        # tuples: the intersections, and the edges.
        for item in terrains_specs:
            # Create a local variable to hold the edges for this terrain.
            local_egdes = []
            for subitem in item[1]:
                # Each integer in the tuple refers to a key in the edges
                # dictionary.  This edge will be added to the list. 
                # Additionally,  this edge's terrains attribute will be updated
                # to hold the terrain we're working on now.
                local_egdes.append(self.edges[subitem])
                self.edges[subitem].terrains.append(self.terrains[item[0]])

            # The same process is repeated for the intersections.
            local_intersections = []
            for subitem in item[2]:
                local_intersections.append(self.intersections[subitem])
                self.intersections[subitem].terrains.append(self.terrains[item[0]])

            # The local lists are converted to tuples and passed to the terrain.
            self.terrains[item[0]].edges = (tuple(local_egdes))
            self.terrains[item[0]].intersections = (tuple(local_intersections))

            # Assign the last landscape and resource number.  (The lists
            # were shuffled, so it's random.) I deduct 1 from the list index,
            # since the dictionary uses keys starting at 1, and lists start at 0.
            self.terrains[item[0]].resource = self.board_resources[item[0]-1]
            self.terrains[item[0]].resource_num = self.roll_numbers[item[0]-1]


        # Using the next list from the board_specs file, the intersections and
        # edges will reference each other.  Additionally, the ports will be added.
        for item in intersections_specs:
            # It uses the same method as above: loops throught he intersections
            # to add a list of edges, and adds self to the edge being processed.
            local_egdes = []
            for subitem in item[1]:
                local_egdes.append(self.edges[subitem])
                self.edges[subitem].intersections.append(self.intersections[item[0]])

            self.intersections[item[0]].edges = local_egdes
            # If that item contains a port, assign it here.
            if len(item) == 3:
                self.intersections[item[0]].port = self.ports[item[2]]

    def buy_dev_card(self,current_player):          
        # pop the card from the dev card and add it to the players dev cards 
        #TODO need to see if you can purchase not sure how to use that method 
        self.card=dev_cards.pop()
        player(current_player).development_cards.insert(card)
        player(current_player).resource_cards.remove('sheep')
        player(current_player).resource_cards.remove('wheat')
        player(current_player).resource_cards.remove('ore')


    
# Create and display the board object.
def main():
    b = Board()
    print(b)
    # for item in b.edges[10].get_neighbors():
    #     print(item.identifier, end = ', ')
    # print('\ndone with\n\n')
    # for item in b.intersections[10].get_neighbors():
    #     print(item.identifier, end = ', ')
    # print('\ndone with\n\n')
    # for item in b.terrains[10].get_neighbors():
    #     print(item.identifier, end = ', ')
    # print('\ndone with\n\n')


if __name__ == '__main__':
    main()
