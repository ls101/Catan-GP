import numpy as np


class CatanPlayer:
    # Initialize the Catan Board with all the options for resources, numbers to be rolled,
    # settlements/roads, port options
    def __init__(self, player_nr):
        self.player_nr = player_nr
        self.unused_items = {
            'roads': 15,
            'settlements': 5,
            'cities': 4
        }
        # Items placed onthe board will be an array containg the index numbers
        # of those items, which are stored in arrays. The index numbers match
        # the numbers on the diagram.
        self.roads = []
        self.settlements = []
        # Note that cities are added by removing said item from the settlements list
        self.cities = []

        # All items owned by the player, but not on the board:
        self.resource_cards = []
        self.development_cards = []
        
        # Game statistics, regarding this player:
        self.road_length = 0
        self.army = 0
        self.victory_points = 0

    def get_input(self, lis) -> int:
        # Will prompt player for a valid number, and return it. If the input is
        # not valid, it will return None. This will be called in a loop, until
        # a valid index is received.
        # the player gets the option to see the board etc.
        print('Please enter the location for placement, as an integer.')
        print('input "s" to [s]how the list')
        position = input()
        # If the player wants to see info, print it
        if position == 's':
            print(lis)
        # Otherwise, validate the input data: must be a digit, and a  valid
        # index for this list.
        elif not position.isdigit:
            print('Input must be an integer. Please try again.')
        elif not 0 < int(position) < len(lis):
            print('Input must be greater than zero and less than {0}. Please try again'.format(len(lis)))
        else:
            # The other issue: if the player can place there because of game
            # rules, will be dealt with outside this method.
            return int(position)


    def set_settlement(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################

        generate buy_settlement input:
        output -- position -- integer 0-54 """
            
        ################################ Insert/Modify CODE HERE ##################################
        # position = int(input('insert argument'))

        # Get, and validate, an integer input. The method will return none for
        # invalid input. A valid index that cannot be used will be reassigned
        # as None. A loop will request an input until a valid one is received.
        position = self.get_input(board.intersections)
        if board.intersections[position] is not None:
            print('That location is not available. Please choose another location.')
            position = None

        while position is None:
            position = self.get_input(board.intersections)
            if board.intersections[position] is not None:
                print('That location is not available. Please choose another location.')
                position = None

        # check if player can place settlement there. Meaning, s/he has a road there
        return position

    def set_city(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################

        output -- genererate buy_city arguments:
        position -- integer 0-53
        """
        ################################ Insert/Modify CODE HERE ##################################

        # position = int(input('insert argument'))

        position = self.get_input(self.settlements)
        if not position in self.settlements:
            print('You do not have a settlement over there. Please choose another location.')
            position = None

        while position is None:
            position = self.get_input(self.settlements)
            if not position in self.settlements:
                print('You do not have a settlement over there. Please choose another location.')
                position = None

        # check if player can place road there. Meaning, s/he has a road next to it
        return position

    def set_road(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################

        output -- generate buy_road arguments:
        position -- integer 0-71
        """
        ################################ Insert/Modify CODE HERE ##################################
        # position = int(input('insert argument'))

        position = self.get_input(board.edges)
        if board.intersections[position] is not None:
            print('That location is already taken. Please choose another location.')
            position = None

        while position is None:
            position = self.get_input(board.edges)
            if board.intersections[position] is not None:
                print('That location is already taken. Please choose another location.')
                position = None

        # check if player can place road there. Meaning, s/he has a road next to it
        return position

    def turn_choice(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################

        output -- integer
        0 -- end turn
        see main for more integer - action correspondance

        """
        ################################ Insert/Modify CODE HERE ##################################
        return 0

    def discard_half(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################
        discard_half output arguments:

        resourses -- np.array([brick, ore, hay, wood, sheep])
                brick -- integer 0-19
                ore -- integer 0-19
                hay -- integer 0-19
                wood --integer 0-19
                sheep --integer 0-19
        """
        ################################ Insert/Modify CODE HERE ##################################

        return np.array([int(input('insert argument')), int(input('insert argument')), int(input('insert argument')),
                         int(input('insert argument')), int(input('insert argument'))])

    def steal_card(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################
        output
        position -- integer 0 - self.number_of_tiles-1
        target_player_nr -- integer 0-3

        """
        ################################ Insert/Modify CODE HERE ##################################
        position, target_player_nr = int(input('insert argument')), int(input('insert argument'))
        return position, target_player_nr

    def play_roads(self, board):
        """

        ################################ Insert/Modify Comments HERE ##################################
        position1 -- integer 0-71
        position2 -- integer 0-71

        """
        ################################ Insert/Modify CODE HERE ##################################
        position1, position2 = int(input('insert argument')), int(input('insert argument'))
        return position1, position2

    def play_plenty(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################
        resource1 -- integer 1-5
        resource2 -- integer 1-5

        """
        ################################ Insert/Modify CODE HERE ##################################

        resource1, resource2 = int(input('insert argument')), int(input('insert argument'))
        return resource1, resource2

    def play_mono(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################
        resource -- integer 1-5
        """
        ################################ Insert/Modify CODE HERE ##################################

        return int(input('insert argument'))

    def trade_bank(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################

        resource_own -- integer 1-5
        resource_bank -- integer 1-5

        """
        ################################ Insert/Modify CODE HERE ##################################
        resource_own, resource_bank = int(input('insert argument')), int(input('insert argument'))
        return resource_own, resource_bank

    def trade_offer(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################
        resources_own -- np.array([brick, ore, hay, wood, sheep])
        target_player_nr -- integer 0-3
        resources_target -- np.array([brick, ore, hay, wood, sheep])
                brick -- integer 0-19
                ore -- integer 0-19
                hay -- integer 0-19
                wood --integer 0-19
                sheep --integer 0-19
        """
        ################################ Insert/Modify CODE HERE ##################################
        resources_own, target_player_nr, resources_target = input('insert argument'),
        input('insert argument'), input('insert argument')

        return resources_own, target_player_nr, resources_target

    def trade_answer(self, board, resources_offered, resources_asked):
        """
        output true or false
        ################################ Insert/Modify Comments HERE ##################################
        resources_offered -- np.array([brick, ore, hay, wood, sheep])
        resources_asked -- np.array([brick, ore, hay, wood, sheep])
                """

        return False

    def start_settelment_second(self, board):
        """
                ################################ Insert/Modify Comments HERE ##################################
        output:
            settle_position -- integer 0-53
            road_position integer 0-71
        """
        ################################ Insert/Modify CODE HERE ##################################

        settle_position, road_position = int(input('insert argument')), int(input('insert argument'))
        return settle_position, road_position

    def start_settelment_first(self, board):
        """
                ################################ Insert/Modify Comments HERE ##################################
        output:
            settle_position -- integer 0-53
            road_position integer 0-71
        """
        ################################ Insert/Modify CODE HERE ##################################

        settle_position, road_position = int(input('insert argument')), int(input('insert argument'))
        return settle_position, road_position


if __name__ == '__main__':
    """
    ################################ Insert/Modify Comments HERE ##################################
    """

    ################################ Insert/Modify CODE HERE ##################################
    p = CatanPlayer(0)
    print(p.player_nr)
    print('Debug complete')
