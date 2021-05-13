import intersectionDetails
import colors

intersections = []
players = [colors.Colors.BLUE,colors.Colors.RED , colors.Colors.BLUE, colors.Colors.YELLOW]

# Each intersection slot will hold their own variables
# the number of the slot, the identifiers of the edges around them
# the identifier of a port - 0 for none
# The identifier(s) of the resources connected to them
# The Player whose settlement/city is places on the spot
class Intersection:
    def __init__(self, number, edges, port, neighbors, resources, board):
        self.number = number
        self.edges = edges
        self.port = port
        # resources are the index of the board space
        # Use this number to find the corresponding number and resource
        # assigned to the slot on the board
        self.resources = resources
        self.neighboring_intersections = neighbors
        self.player = None

    # Set the player whose piece is built on the intersection
    def set_player(self, player):
        if not self.check_neighbors(player):
            self.player = player

    # Check_neighbors will check if the neighboring intersections
    # are occupied by another player and return False if the player
    # is not allowed to place a settlement in the spot
    def check_neighbors(self, player):
        for i in self.neighboring_intersections:
            # if the player is assigned and different than the player
            # trying to place the piece, return False to not allow
            if intersections[i].player and not intersections[i].player == player:
                return False
        return True

    # When a number is spun you can loop through all of the intersections
    # with that number and return the number of the player who should get
    # the resource. This may be better done from the players end to have
    # each player check if they are connected to one of the resources.
    def return_resources(self, number_spun):
        if number_spun == self.number and self.player is not None:
            return self.player


# Edges - each edge/road will have a number and status
# Status - available, non-existent(0), player # for a taken road
class Edges:
    def __init__(self, number):
        self.number = number
        if number == 0:
            self.status = "non-existent"
        else:
            self.status = "available"

    def set_player(self, player_number):
        self.status = player_number

    # def check_edges(self):


def create_intersections(board):
    for details in intersectionDetails.intersections:
        number, edges, port, neighbors, resources = details[0], details[1], details[2], details[3], details[4]
        intersections.append(Intersection(number, edges, port, neighbors, resources))
    return intersections


class Terrain:
    def __init__(self, number, resource, board):
        self.number = number
        self.resource = resource,
        # filter the intersections who are associated with that terrain
        self.board = board
        self.intersections = filter(lambda x: self.number == x.resource,
                                    self.board.intersections)
        self.edges = []

    def __str__(self):
        for intersection in self.intersections:
            if intersection.player is not None:
                color = players[intersection.player]
                settlement_text = "s"
            else:
                color = colors.Colors.BLACK
                settlement_text = "_"
            string_output = (f" _{color}{settlement_text}{color.Colors.BLACK}_ ")
            string_output += "\n/"
 # /\\ /\\ /\\ \n'
 #        s += '  |01|02|03| \n'
 #        s += '   \\/ \\/ \\/ \n'


