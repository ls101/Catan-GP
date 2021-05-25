from board_components import RESOURCE_NAMES
import numpy as np
from cards import *
import constants
import board as board

prices = constants.PRICES
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
        # Items placed on the board will be an array containg the index numbers
        # of those items, which are stored in arrays. The index numbers match
        # the numbers on the diagram.
        self.roads = []
        self.settlements = []
        # Note that cities are added by removing said item from the settlements list
        self.cities = []
        # port where the player has a settlement
        self.ports = []

        # All items owned by the player, but not on the board:
        self.resource_cards = ResourceCards()
        self.development_cards = Cards()
        
        # Game statistics, regarding this player:
        self.road_length = 0
        self.army = 0
        self.victory_points = 0

    # Find valid locations for settlements based on current settlements
    # and roads - the new settlement must be attached to the player's
    # road and occupier must be None
    def get_valid_settlements(self, board):
        valid_settlements = []
        # check if the intersection attached to the player's roads
        # is available
        for road in self.roads:
            for intersection in road.intersections:
                if intersection.occupier is None:
                    valid_settlements.append(intersection.identifier)
        return valid_settlements

    def get_valid_roads(self, board):
        valid_roads = []
        # check if the road is attached to the player's roads
        # and is available
        for road in self.roads:
            for neighbor in road.get_neighbors():
                if road.occupier is None:
                    valid_roads.append(neighbor.identifier)
        return valid_roads

    # Takes a list of valid positions to place object and asks for input
    # If the input is valid, returns the position
    # Otherwise the player can try again
    def get_index_input(self, valid_positions):
        while True:
            position = int(input('Choose a location from the list'))
            if position in valid_positions:
                return position
            else:
                print("Please choose a valid option")

    def can_buy(self, type_to_buy):
        # Checks if the player has resources to buy
        # Self.resource_cards is a dictionary of players cards - resource_number : amount_of_resource
        # Find which resources are needed to buy type_to_buy
        needed_to_buy = constants.PRICES[type_to_buy]
        # Check if player has those resources in their cards
        for key in needed_to_buy:
            # if the player does not have enough of one
            # type of resource, they can not buy that type of item
            if self.resource_cards.resource_cards[key] < needed_to_buy[key]:
                return False
        return True

    def purchase_settlement(self, position, board, override):
        # Add the position to the players list of settlements
        self.settlements.append(board.intersections[position])
        # Remove resource cards that were needed to purchase settlement
        if not override:
            for key in constants.PRICES['settlement']:
                self.resource_cards.resource_cards[key] -= constants.PRICES['settlement'][key]
        # Add point for building settlement
        self.victory_points += 1

    def purchase_city(self, position, board):
        # Remove the position from settlement and add to cities
        for i in self.settlements:
            if i.identifier == position:
                self.settlements.remove(i)
        self.cities.append(board.intersections[position])
        # Remove resource cards that were needed to purchase city
        for key in constants.PRICES['city']:
            self.resource_cards.resource_cards[key] -= constants.PRICES['city'][key]
        # Add two points for building a city
        self.victory_points += 2

    def purchase_road(self, position, board, override):
        # Add the position to the players list of road
        self.roads.append(board.edges[position])
        # Remove resource cards that were needed to purchase road
        if not override:
            for key in constants.PRICES['road']:
                self.resource_cards.resource_cards[key] -= constants.PRICES['road'][key]

    # Find valid locations for settlements based on current settlements
    # and roads - the new settlement must be attached to the player's
    # road and occupier must be None
    # Override used for first settlements when no resource cards are taken
    def set_settlement(self, board, override=False):
        # check if player has resources to buy settlement
        if self.can_buy('settlement') or override:
            # find valid places to put settlements
            valid_settlements = self.get_valid_settlements(board)
            # print list of valid settlements to choose from to build on
            print(valid_settlements)
            # get a valid position to place the settlement
            position = self.get_index_input(valid_settlements)
            # Purchase the settlement and trade in cards
            self.purchase_settlement(position, board, override)
            return position

    def set_city(self, board):
        # check if player has resources to buy city
        if self.can_buy('city'):
            # find valid places to put cities
            valid_cities = []
            for settlement in self.settlements:
                valid_cities.append(settlement.identifier)
            # print list of valid cities to choose from to build on
            print(valid_cities)
            # get a valid position to place the city
            position = self.get_index_input(valid_cities)
            # Purchase the city and trade in cards
            self.purchase_city(position, board)
            return position

    def set_road(self, board, override=False):
        # check if player has resources to buy settlement
        if self.can_buy('road') or override:
            # find valid places to put settlements
            valid_roads = self.get_valid_roads(board)
            # print list of valid roads to choose from to build on
            print(valid_roads)
            # get a valid position to place the road
            position = self.get_index_input(valid_roads)
            # Purchase the road and trade in cards
            self.purchase_road(position, board, override)
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

    def offer_input(self, key, value):
        try:
            offer = int(input('How many {0} cards?'.format(key)))
        except:
            print('Input must be numeric. Try again.')
            return self.offer_input(key, value)
        else:
            # No exception, meaning input is an integer, now check if it's a valid number.
            if not 0 <= offer <= value:
                print('You must submit a non-negative number, not greater than {0}'.format(value))
                return self.offer_input(key, value)
            else:
                # A valid number is returned
                return offer


    def offer_cards(self):
        # For trade offers and for discarding
        print(self.resource_cards)
        offering = {}
        for key, value in self.resource_cards.resource_cards.items():
            # Iterate over the dictionary, but only offer to trade/discard
            # cards the player has. Meaning, value is not zero.
            if value > 0:
                # get a valid offer, meaning how many cards of that type to discard/trade
                offer = self.offer_input(key, value)
                print(offer)
                if offer > 0:
                    offering[key] = offer
        return offering


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
        print('Robber activated!')
        if self.resource_cards.get_discard_num() > 0:
            return self.offer_cards()

        # return np.array([int(input('insert argument')), int(input('insert argument')), int(input('insert argument')),
        #                  int(input('insert argument')), int(input('insert argument'))])

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

    def ports_trade(self, key):
        # Checks if a player has a port; this allows better trading terms
        # when trading with the bank.
        resource_search = RESOURCE_NAMES.index(key)
        if resource_search in self.ports:
            return 2
        elif 0 in self.ports:
            return 3
        else:
            return 4

    def trade_bank(self, board):
        """
        ################################ Insert/Modify Comments HERE ##################################

        resource_own -- integer 1-5
        resource_bank -- integer 1-5

        """
        ################################ Insert/Modify CODE HERE ##################################
        resource_own, resource_bank = int(input('insert argument')), int(input('insert argument'))

        if resource_own == resource_bank:
            # error message
            pass
        else:
            # Determine how many cards the palyer needs to give to the bank
            give = self.ports_trade(resource_own)
            # Ensure the player has those cards
            if self.resource_cards.resource_cards[resource_own] >= give:
                return resource_own, resource_bank, give
            else:
                # error message
                pass

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
        settle_position = self.get_index_input(board.intersections)
        if board.intersections[settle_position] is not None:
            print('That location is not available. Please choose another location.')
            settle_position = None
        # Repeat the above code, until a valid input is returned
        while settle_position is None:
            settle_position = self.get_index_input(board.intersections)
            if board.intersections[settle_position] is not None:
                print('That location is not available. Please choose another location.')
                settle_position = None


        # Now, get the position of a road next to the chosen settlement position
        road_position = self.get_index_input(settle_position.edges)
        if board.edges[road_position] is not None:
            print('That location is already taken. Please choose another location.')
            road_position = None

        while road_position is None:
            road_position = self.get_index_input(settle_position.edges)
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
    b = board.Board()
    p.roads.append(b.edges[1])
    p.settlements.append(b.intersections[1])
    print(p.resource_cards)
    # print(p.discard_half())
    # test_list = [10,20,30,40,50]
    # p.get_input_by_index(test_list)
    # p.get_input_by_value(test_list)
    p.set_settlement(b)
    print(p.resource_cards)
    print('Debug complete')
