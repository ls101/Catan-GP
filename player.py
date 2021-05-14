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
        # Players can place settlements only where they have a road. This will
        # be tracked here.
        self.valid_settlements = []

        # All items owned by the player, but not on the board:
        self.resource_cards = []
        self.development_cards = []
        
        # Game statistics, regarding this player:
        self.road_length = 0
        self.army = 0
        self.victory_points = 0

    def get_input_by_index(self, lis) -> int:
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
            return int(position)


    def get_input_by_value(self, lis) -> int:
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
        # Otherwise, validate the input data: must be a digit, and an integer
        # that is in this list.
        elif not position.isdigit:
            print('Input must be an integer. Please try again.')
        elif not int(position) in lis:
            print('Your chosen number is not in the list. Please try again.')
        else:
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
        position = self.get_input_by_value(self.valid_settlements)
        if board.intersections[position] is not None:
            print('That location is not available. Please choose another location.')
            position = None

        while position is None:
            position = self.get_input_by_value(self.valid_settlements)
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

        position = self.get_input_by_value(self.settlements)
        if not position in self.settlements:
            print('You do not have a settlement over there. Please choose another location.')
            position = None

        while position is None:
            position = self.get_input_by_value(self.settlements)
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


        # The following code must be altered; the list does not follow the game rules

        # Initialize a temporary list for where the player can place a road
        lis = []
        for item in self.settlements:
            for element in item.edges:
                if board.edges[element] is None: lis.append(element)
        for item in self.cities:
            for element in item.edges:
                if board.edges[element] is None: lis.append(element)

        # Get a valid position where to place the road
        position = self.get_input_by_value(lis)
        if board.intersections[position] is not None:
            print('That location is already taken. Please choose another location.')
            position = None

        while position is None:
            position = self.get_input_by_value(lis)
            if board.intersections[position] is not None:
                print('That location is already taken. Please choose another location.')
                position = None

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

        # settle_position, road_position = int(input('insert argument')), int(input('insert argument'))
        # This is really the same as the first settlement
        settle_position, road_position = self.start_settelment_first(self, board)
        return settle_position, road_position

    def start_settelment_first(self, board):
        # Can add:
        # if an intersection's roads are all taken, it should not be a valid option
        """
                ################################ Insert/Modify Comments HERE ##################################
        output:
            settle_position -- integer 0-53
            road_position integer 0-71
        """
        ################################ Insert/Modify CODE HERE ##################################

        # settle_position, road_position = int(input('insert argument')), int(input('insert argument'))

        # Get, and validate, an integer input. The method will return none for
        # invalid input. A valid index that cannot be used will be reassigned
        # as None. A loop will request an input until a valid one is received.
        settle_position = self.get_input_by_index(board.intersections)
        if board.intersections[settle_position] is not None:
            print('That location is not available. Please choose another location.')
            settle_position = None
        # Repeat the above code, until a valid input is returned
        while settle_position is None:
            settle_position = self.get_input_by_index(board.intersections)
            if board.intersections[settle_position] is not None:
                print('That location is not available. Please choose another location.')
                settle_position = None


        # Now, get the position of a road next to the chosen settlement position
        road_position = self.get_input_by_value(settle_position.edges)
        if board.edges[road_position] is not None:
            print('That location is already taken. Please choose another location.')
            road_position = None

        while road_position is None:
            road_position = self.get_input_by_value(settle_position.edges)
            if board.edges[road_position] is not None:
                print('That location is already taken. Please choose another location.')
                road_position = None

        # Return the two integers
        return settle_position, road_position


if __name__ == '__main__':
    """
    ################################ Insert/Modify Comments HERE ##################################
    """

    ################################ Insert/Modify CODE HERE ##################################
    p = CatanPlayer(0)
    print(p.player_nr)
    print('Debug complete')
