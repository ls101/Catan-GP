import numpy as np
import random

RESOURCE_NAMES = ["desert", "brick", "ore", "hay", "wood", "sheep"]

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
            if self.ports == 3:
                s += ' [General port 3:1]'
            else:
                s += ' [{0} port 2:1]'.format(self.ports)
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
        has_robber=False
    ) -> None:
        self.identifier = identifier
        self.resource_num = resource_num
        self.resource = resource
        self.edges = edges
        self.intersections = intersections
        self.has_robber = has_robber

    def __str__(self) -> str:
        s = str(self.identifier) + '\n'
        s += 'Landscape: {0}\n'.format(
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


# The ports are just a list now, although it really should be an object.
# For now, if it's a number 3, it's a general port; otherwise, its
# number is 2.  It should be changed eventually to an object containing
# two attributes: number and type.  I shuffle the ports, since this is
# how I see it in the game link you sent and it's not a big deal.
ports = [3, 3, 3, 3, 'Brick', 'Lumber', 'Ore', 'Grain', 'Wool']
random.shuffle(ports)


def main():
    i = Intersection(0)
    print(i)
    e = Edge(0)
    print(e)
    t = Terrain(0, 0, 1)
    print(RESOURCE_NAMES[t.resource])


if __name__ == '__main__':
    main()
