import numpy as np
import random

RESOURCE_NAMES = ["desert", "brick", "ore", "hay", "wood", "sheep"]
PORTS_NAMES = ["3:1", "2brick:1", "2ore:1", "2hay:1", "2wood:1", "2sheep:1"]

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

#  The default resource_num of zero references the ocean surrounding the
# island, and bordering some objects.


class Edge:
    # occupier references the road that players can place on the edge
    # during the game.  Since this is all that really matters in the
    # game, the string method returns this property only.
    def __init__(
        self,
        identifier,
        intersections=(0, 0),
        terrains=(0, 0),
        occupier=None
    ) -> None:
        self.identifier = identifier
        self.intersections = intersections
        self.terrains = terrains
        self.occupier = occupier

    def __str__(self) -> str:
        if self.occupier is None:
            return 'available'
        else:
            return self.occupier

    def get_neighbors(self):
        for edge in self.intersections:
            # return all neighboring roads
            pass


class Intersection:
    # occupier references the settlements and cities that players can
    # place on the intersection during the game.  And intersection that
    # cannot have a new settlement (because an adjacent intersection is
    # settled) will be marked as restricted.  The string method returns
    # this info, as well as any ports.
    def __init__(
        self,
        identifier,
        edges=(0, 0, 0),
        occupier=None,
        ports=None
    ) -> None:
        self.identifier = identifier
        self.edges = edges
        self.occupier = occupier
        self.ports = ports

    def __str__(self) -> str:
        if self.occupier is None:
            s = 'available'
        else:
            s = self.occupier
        if self.ports is not None:
            s += ' [{0} port]'.format(PORTS_NAMES[self.ports])
        return s

    def get_next():
        pass


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
        pass


def main():
    i = Intersection(0)
    print(i)
    e = Edge(0)
    print(e)
    t = Terrain(0, 0, 1)
    print(t)
    print(RESOURCE_NAMES[t.resource])


if __name__ == '__main__':
    main()
