import random
from board_components import Terrain, Edge, Intersection, ports


class Board:
    def __init__(self):
        # Initialize a list for each attribute type.
        self.edges = self.initialize_edges()
        self.intersections = self.initialize_intersections()
        self.terrains = self.initialize_terrains()
        # Assign the correct attributes for each attribute.
        self.assign()

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
    def a_edge(self, identifier, intersection, terrain) -> None:
        # Identify the correct objects from the initialized lists, based
        # on the values of the tuple parameters.
        a = self.intersections[intersection[0]]
        b = self.intersections[intersection[1]]
        c = self.terrains[terrain[0]]
        d = self.terrains[terrain[1]]
        # Pass the objects, as tuples, to reassign the attributes of the
        # object.
        self.edges[identifier].intersections = (a, b)
        self.edges[identifier].terrain = (c, d)

    def a_intersection(self, identifier, edge, ports=None) -> None:
        # Identify the correct objects from the initialized lists, based
        # on the values of the tuple parameters.
        a = self.edges[edge[0]]
        b = self.edges[edge[1]]
        c = self.edges[edge[2]]
        # Pass the objects, as tuples, to reassign the attributes of the
        # object.
        self.intersections[identifier].edges = (a, b, c)
        self.intersections[identifier].ports = ports

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

    def a_terrain(
        self,
        identifier,
            edge=(0, 0, 0, 0, 0, 0),
            intersection=(0, 0, 0, 0, 0, 0),
    ) -> None:
        # Identify the correct objects from the initialized lists, based
        # on the values of the tuple parameters.
        a = self.edges[edge[0]]
        b = self.edges[edge[1]]
        c = self.edges[edge[2]]
        d = self.edges[edge[3]]
        e = self.edges[edge[4]]
        f = self.edges[edge[5]]
        g = self.intersections[intersection[0]]
        h = self.intersections[intersection[1]]
        i = self.intersections[intersection[2]]
        j = self.intersections[intersection[3]]
        k = self.intersections[intersection[4]]
        m = self.intersections[intersection[5]]

        # Pass the objects, as tuples, to reassign the attributes of the
        # object.
        self.terrains[identifier].edges = (a, b, c, d, e, f)
        self.terrains[identifier].intersections = (g, h, i, j, k, m)

        # Assign the last landscape and resource number.  (The lists
        # were shuffled, so it's random.)  The dessert doesn't have a
        # resource number, and it has the robber.
        landscape = self.landscapes.pop()
        self.terrains[identifier].landscape = landscape
        self.terrains[identifier].resource = Terrain.resources[landscape]
        if landscape == 'Dessert':
            self.terrains[identifier].has_robber = True
            self.terrains[identifier].resource_num = None
        else:
            self.terrains[identifier].resource_num = self.resource_nums.pop()

    def assign(self):
        # Now, assign all attributes; board will be set up fully after
        # this is called.
        self.a_edge(1, (1, 2), (0, 1))
        self.a_edge(2, (2, 3), (0, 1))
        self.a_edge(3, (3, 4), (0, 2))
        self.a_edge(4, (4, 5), (0, 2))
        self.a_edge(5, (5, 6), (0, 3))
        self.a_edge(6, (6, 7), (0, 3))
        self.a_edge(7, (1, 9), (0, 1))
        self.a_edge(8, (3, 11), (1, 2))
        self.a_edge(9, (5, 13), (2, 3))
        self.a_edge(10, (7, 15), (0, 3))
        self.a_edge(11, (8, 9), (0, 4))
        self.a_edge(12, (9, 10), (1, 4))
        self.a_edge(13, (10, 11), (1, 5))
        self.a_edge(14, (11, 12), (2, 5))
        self.a_edge(15, (12, 13), (2, 6))
        self.a_edge(16, (13, 14), (3, 6))
        self.a_edge(17, (14, 15), (3, 7))
        self.a_edge(18, (15, 16), (0, 7))
        self.a_edge(19, (8, 18), (0, 4))
        self.a_edge(20, (10, 20), (4, 5))
        self.a_edge(21, (12, 22), (5, 6))
        self.a_edge(22, (14, 24), (6, 7))
        self.a_edge(23, (16, 26), (0, 7))
        self.a_edge(24, (17, 18), (0, 8))
        self.a_edge(25, (18, 19), (4, 8))
        self.a_edge(26, (19, 20), (4, 9))
        self.a_edge(27, (20, 21), (5, 9))
        self.a_edge(28, (21, 22), (5, 10))
        self.a_edge(29, (22, 23), (6, 10))
        self.a_edge(30, (23, 24), (6, 11))
        self.a_edge(31, (24, 25), (7, 11))
        self.a_edge(32, (25, 26), (7, 12))
        self.a_edge(33, (26, 27), (0, 12))
        self.a_edge(34, (17, 28), (0, 8))
        self.a_edge(35, (19, 30), (8, 9))
        self.a_edge(36, (21, 32), (9, 10))
        self.a_edge(37, (23, 34), (10, 11))
        self.a_edge(38, (25, 36), (11, 12))
        self.a_edge(39, (27, 38), (0, 12))
        self.a_edge(40, (28, 29), (0, 8))
        self.a_edge(41, (29, 30), (8, 13))
        self.a_edge(42, (30, 31), (9, 13))
        self.a_edge(43, (31, 32), (9, 14))
        self.a_edge(44, (32, 33), (10, 14))
        self.a_edge(45, (33, 34), (10, 15))
        self.a_edge(46, (34, 35), (11, 15))
        self.a_edge(47, (35, 36), (11, 16))
        self.a_edge(48, (36, 37), (12, 16))
        self.a_edge(49, (37, 38), (0, 12))
        self.a_edge(50, (29, 39), (0, 13))
        self.a_edge(51, (31, 41), (13, 14))
        self.a_edge(52, (33, 43), (14, 15))
        self.a_edge(53, (35, 46), (15, 16))
        self.a_edge(54, (37, 47), (0, 16))
        self.a_edge(55, (39, 40), (0, 13))
        self.a_edge(56, (40, 41), (13, 17))
        self.a_edge(57, (41, 42), (14, 17))
        self.a_edge(58, (42, 43), (14, 18))
        self.a_edge(59, (43, 44), (15, 18))
        self.a_edge(60, (44, 45), (15, 19))
        self.a_edge(61, (45, 46), (16, 19))
        self.a_edge(62, (46, 47), (0, 16))
        self.a_edge(63, (40, 48), (0, 17))
        self.a_edge(64, (42, 50), (17, 18))
        self.a_edge(65, (44, 52), (18, 19))
        self.a_edge(66, (46, 54), (0, 19))
        self.a_edge(67, (48, 49), (0, 17))
        self.a_edge(68, (49, 50), (0, 17))
        self.a_edge(69, (50, 51), (0, 18))
        self.a_edge(70, (51, 52), (0, 18))
        self.a_edge(71, (52, 53), (0, 19))
        self.a_edge(72, (53, 54), (0, 19))

        self.a_intersection(1, (0, 1, 7), ports[8])
        self.a_intersection(2, (0, 2, 1), ports[8])
        self.a_intersection(3, (2, 3, 8))
        self.a_intersection(4, (0, 4, 3), ports[0])
        self.a_intersection(5, (4, 5, 9), ports[0])
        self.a_intersection(6, (0, 6, 5))
        self.a_intersection(7, (6, 0, 10))
        self.a_intersection(8, (0, 11, 19), ports[7])
        self.a_intersection(9, (7, 12, 11))
        self.a_intersection(10, (12, 13, 20))
        self.a_intersection(11, (8, 14, 13))
        self.a_intersection(12, (14, 15, 21))
        self.a_intersection(13, (9, 16, 15))
        self.a_intersection(14, (16, 17, 22))
        self.a_intersection(15, (10, 18, 17), ports[1])
        self.a_intersection(16, (18, 0, 23), ports[1])
        self.a_intersection(17, (0, 24, 34))
        self.a_intersection(18, (19, 25, 24), ports[7])
        self.a_intersection(19, (25, 26, 35))
        self.a_intersection(20, (20, 27, 26))
        self.a_intersection(21, (27, 28, 36))
        self.a_intersection(22, (21, 29, 28))
        self.a_intersection(23, (29, 30, 37))
        self.a_intersection(24, (22, 31, 30))
        self.a_intersection(25, (31, 32, 38))
        self.a_intersection(26, (23, 33, 32))
        self.a_intersection(27, (33, 0, 39), ports[2])
        self.a_intersection(28, (34, 40, 0))
        self.a_intersection(29, (40, 41, 50), ports[6])
        self.a_intersection(30, (35, 42, 41))
        self.a_intersection(31, (42, 43, 51))
        self.a_intersection(32, (36, 44, 43))
        self.a_intersection(33, (44, 45, 52))
        self.a_intersection(34, (37, 46, 45))
        self.a_intersection(35, (46, 47, 53))
        self.a_intersection(36, (38, 48, 47))
        self.a_intersection(37, (48, 49, 54))
        self.a_intersection(38, (39, 0, 49), ports[2])
        self.a_intersection(39, (50, 55, 0), ports[6])
        self.a_intersection(40, (55, 56, 63))
        self.a_intersection(41, (51, 57, 56))
        self.a_intersection(42, (57, 58, 64))
        self.a_intersection(43, (52, 59, 58))
        self.a_intersection(44, (59, 60, 65))
        self.a_intersection(45, (53, 61, 60))
        self.a_intersection(46, (61, 62, 66), ports[3])
        self.a_intersection(47, (54, 0, 62), ports[3])
        self.a_intersection(48, (63, 67, 0), ports[5])
        self.a_intersection(49, (67, 68, 0), ports[5])
        self.a_intersection(50, (64, 69, 68))
        self.a_intersection(51, (69, 70, 0), ports[4])
        self.a_intersection(52, (65, 71, 70), ports[4])
        self.a_intersection(53, (71, 72, 0))
        self.a_intersection(54, (66, 0, 72))

        # Edges start at top-right, clockwise, end at top-left.
        # Intersections start at top-center, clockwise.
        self.a_terrain(1, (2, 8, 13, 12, 7, 1), (2, 3, 11, 10, 9, 1))
        self.a_terrain(2, (4, 9, 15, 14, 8, 3), (4, 5, 13, 12, 11, 3))
        self.a_terrain(3, (6, 10, 17, 16, 9, 5), (6, 7, 15, 14, 13, 5))
        self.a_terrain(4, (12, 20, 26, 25, 19, 11), (9, 10, 20, 19, 18, 8))
        self.a_terrain(5, (14, 21, 28, 27, 20, 13), (11, 12, 22, 21, 20, 10))
        self.a_terrain(6, (16, 22, 30, 29, 21, 15), (13, 14, 24, 23, 22, 12))
        self.a_terrain(7, (18, 23, 32, 31, 22, 17), (15, 16, 26, 25, 24, 14))
        self.a_terrain(8, (25, 35, 41, 40, 34, 24), (18, 19, 30, 29, 28, 17))
        self.a_terrain(9, (27, 36, 43, 42, 35, 26), (20, 21, 32, 31, 30, 19))
        self.a_terrain(10, (29, 37, 45, 44, 36, 28), (22, 23, 34, 33, 32, 21))
        self.a_terrain(11, (31, 38, 47, 46, 37, 30), (24, 25, 36, 35, 34, 23))
        self.a_terrain(12, (33, 39, 49, 48, 38, 32), (26, 27, 38, 37, 36, 25))
        self.a_terrain(13, (42, 51, 56, 55, 50, 41), (30, 31, 41, 40, 39, 29))
        self.a_terrain(14, (44, 52, 58, 57, 51, 43), (32, 33, 43, 42, 41, 31))
        self.a_terrain(15, (46, 53, 60, 59, 52, 45), (34, 35, 45, 44, 43, 33))
        self.a_terrain(16, (48, 54, 62, 61, 53, 47), (36, 37, 47, 46, 45, 35))
        self.a_terrain(17, (57, 64, 68, 67, 63, 56), (41, 42, 50, 49, 48, 40))
        self.a_terrain(18, (59, 65, 70, 69, 64, 58), (43, 44, 52, 51, 50, 42))
        self.a_terrain(19, (61, 66, 72, 71, 65, 60), (45, 46, 54, 53, 52, 44))


# Create and display the board object.
def main():
    b = Board()
    print(b)


if __name__ == '__main__':
    main()
