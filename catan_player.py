from cards import *
import constants

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
        # Players can place settlements only where they have a road. This will
        # be tracked here.
        # self.valid_settlements = []

        # All items owned by the player, but not on the board:
        self.resource_cards = ResourceCards()
        self.development_cards = Cards()
        
        # Game statistics, regarding this player:
        self.road_length = 0
        self.army = 0
        self.victory_points = 0

    # def get_input_by_index(self, lis) -> int:
    #     # Will prompt player for a valid number, and return it. If the input is
    #     # not valid, it will return None. This will be called in a loop, until
    #     # a valid index is received.
    #     # the player gets the option to see the board etc.
    #     print('Please enter the location for placement, as an integer.')
    #     print('input "s" to [s]how the list')
    #     position = input()
    #     # If the player wants to see info, print it
    #     if position == 's':
    #         print(lis)
    #         return self.get_input_by_index(lis)
    #     # Otherwise, validate the input data: must be a digit, and a  valid
    #     # index for this list.
    #     elif not position.isdigit():
    #         print('Input must be an integer. Please try again.')
    #         return self.get_input_by_index(lis)
    #     elif not 0 < int(position) < len(lis):
    #         print('Input must be greater than zero and less than {0}. Please try again'.format(len(lis)))
    #         return self.get_input_by_index(lis)
    #     else:
    #         return int(position)
    #
    #
    # def get_input_by_value(self, lis) -> int:
    #     # Will prompt player for a valid number, and return it. If the input is
    #     # not valid, it will return None. This will be called in a loop, until
    #     # a valid index is received.
    #     # the player gets the option to see the board etc.
    #     print('Please enter the location for placement, as an integer.')
    #     print('input "s" to [s]how the list')
    #     position = input()
    #     # If the player wants to see info, print it
    #     if position == 's':
    #         print(lis)
    #         return self.get_input_by_value(lis)
    #     # Otherwise, validate the input data: must be a digit, and an integer
    #     # that is in this list.
    #     elif not position.isdigit():
    #         print('Input must be an integer. Please try again.')
    #         return self.get_input_by_value(lis)
    #     elif not int(position) in lis:
    #         print('Your chosen number is not in the list. Please try again.')
    #         return self.get_input_by_value(lis)
    #     else:
    #         return int(position)

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

    def discard_half(self):
        
        """ 
        The output is a dictionary, NOT an np array
         """
        print('Robber activated!')
        num = self.resource_cards.get_discard_num()
        if num > 0:
            offer = self.offer_cards()
            if sum(offer.values()) == num:
                return offer
            else:
                pass
        else:
            return None


if __name__ == '__main__':
    
    p = CatanPlayer(0)
    print(p.player_nr)
    # print(p.discard_half())
    # test_list = [10,20,30,40,50]
    # p.get_input_by_index(test_list)
    # p.get_input_by_value(test_list)
    print('Debug complete')
