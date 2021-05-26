import constants

RESOURCE_NAMES = constants.RESOURCE_NAMES
PORTS_NAMES = constants.PORTS_NAMES
# This module defines the components of the board: terrains, edges
# between the terrains, and intersections connecting the edges.  To
# enable all game functions, each component is an object, and has the
# other components as attributes.  Since I cannot assign an object
# before creating it, the objects are initialized with default
# attributes (the number zero). The object attributes are reassigned
# thereafter.  Since there can be several pointers to a single object,
# it does not matter in which order these are assigned; even if it's
# assigned when the attributes are still integers, when all is done, all
# attributes will be correct.


class Edge:
    # occupier references the road that players can place on the edge
    # during the game.  Since this is all that really matters in the
    # game, the string method returns this only property and its identifier.
    def __init__(
        self,
        identifier,
        intersections=[],
        terrains=[],
        occupier=None
    ) -> None:
        self.identifier = identifier
        self.intersections = intersections
        self.terrains = terrains
        self.occupier = occupier

    def __str__(self) -> str:
        s = str(self.identifier) + ': '
        if self.occupier is None:
            s += 'available'
        else:
            s += self.occupier
        return s

    def get_neighbors(self):
        neighbors = []
        # return all neighboring roads
        for intersection in self.intersections:
            for edge in intersection.edges:
                if edge != self:
                    neighbors.append(edge)
        return set(neighbors)


class Intersection:
    # occupier references the settlements and cities that players can
    # place on the intersection during the game.  And intersection that
    # cannot have a new settlement (because an adjacent intersection is
    # settled) will be marked as restricted.  The string method returns
    # this info, as well as any port.
    def __init__(
        self,
        identifier,
        edges=[],
        terrains=[],
        occupier=None,
        port=None
    ) -> None:
        self.identifier = identifier
        self.edges = edges
        self.terrains = terrains
        self.occupier = occupier
        self.port = port

    def __str__(self) -> str:
        s = str(self.identifier) + ': '
        if self.occupier is None:
            s += 'available'
        elif self.occupier[0] < 0:
            s += 'restricted'
        else:
            s += self.occupier[1]
        if self.port is not None:
            s += ' [{0} port]'.format(PORTS_NAMES[self.port])
        return s

    def get_neighbors(self):
        neighbors = []
        # return all neighboring roads
        for edge in self.edges:
            for intersection in edge.intersections:
                if intersection != self:
                    neighbors.append(intersection)
        return set(neighbors)


class Terrain:

    def __init__(
        self,
        identifier,
        resource_num,
        resource,
        edges=(0, 0, 0, 0, 0, 0),
        intersections=(0, 0, 0, 0, 0, 0),
    ) -> None:
        self.identifier = identifier
        self.resource_num = resource_num
        self.resource = resource
        self.edges = edges
        self.intersections = intersections

    def __str__(self) -> str:
        s = str(self.identifier) + '\n'
        s += 'Resource: {0}\n'.format(
            RESOURCE_NAMES[self.resource],
        )
        s += 'Resource number: {0}\n'.format(
            self.resource_num
            )
        s += 'From top, clockwise: \n'
        for x in range(6):
            s += str(self.intersections[x]) + ' (intersection), '\
                + str(self.edges[x]) + ' (edge), '
        s += '\n'
        return s

    def get_neighbors(self):
        neighbors = []
        # return all neighboring roads
        for edge in self.edges:
            for terrain in edge.terrains:
                if terrain != self:
                    neighbors.append(terrain)
        return set(neighbors)


def main():
    pass
    # i = Intersection(0)
    # print(i)
    # e = Edge(0)
    # print(e)
    # t = Terrain(0, 0, 1)
    # print(t)
    # print(RESOURCE_NAMES[t.resource])
    # e.get_neighbors()
    # i.get_neighbors()
    # t.get_neighbors()


if __name__ == '__main__':
    main()
