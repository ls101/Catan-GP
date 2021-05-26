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
        # Items placed on the board will be an array containing the index numbers
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
        self.development_cards = DevCards()

        # Game statistics, regarding this player:
        # self.road_length = 0
        self.army = 0
        self.victory_points = 0

        # Resources that correspond to where the player has settlements/cities - double resources for cities
        # Tuple - resource_num, resource_type
        self.resources = []

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
        print(valid_positions)
        while True:
            try:
                position = int(input("Choose a positon(number) from the list"))
                if position in valid_positions:
                    return position
                else:
                    print("Invalid choice, try again")
            except:
                print("Invalid input, try again")

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
        if self.unused_items[type_to_buy] <= 0:
            return False
        return True

    def purchase_settlement(self, position, board, override):
        # Add the position to the players list of settlements
        self.settlements.append(board.intersections[position])

        # Add the resources for where the settlement is places
        for terrain in board.intersections[position].terrains:
            self.resources.append((terrain.resource_num, terrain.resource))

        # Add ports - if the intersection has a port, add it to player's ports
        if board.intersections[position].port is not None:
            self.ports.append(board.intersections[position].port)

        # Remove resource cards that were needed to purchase settlement
        if not override:
            for key in constants.PRICES['settlement']:
                board.cards.move_cards(bank, {key, constants.PRICES['settlement'][key] * -1})
        # Add point for building settlement
        self.victory_points += 1
        # Remove settlement from unused items
        self.unused_items['settlements'] -= 1

    def purchase_city(self, position, board):
        # Remove the position from settlement and add to cities
        for i in self.settlements:
            if i.identifier == position:
                self.settlements.remove(i)
        self.cities.append(board.intersections[position])
        # Add the resources for where the city is places (twice)
        for terrain in board.intersections[position].terrains:
            self.resources.append((terrain.resource_num, terrain.resource))
            self.resources.append((terrain.resource_num, terrain.resource))
        # Remove resource cards that were needed to purchase city
        for key in constants.PRICES['city']:
            board.cards.move_cards(bank, {key, constants.PRICES['city'][key] * -1})
        # Add two points for building a city
        self.victory_points += 2
        # Remove city from unused and put back settlement
        self.unused_items['cities'] -= 1
        self.unused_items['settlements'] += 1

    def purchase_road(self, position, board, override):
        # Add the position to the players list of road
        self.roads.append(board.edges[position])
        # Remove resource cards that were needed to purchase road
        if not override:
            for key in constants.PRICES['road']:
                board.cards.move_cards(bank, {key, constants.PRICES['city'][key] * -1})
        # Remove road from unused
        self.unused_items['roads'] -= 1

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
        else:
            return None

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
        else:
            return None

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
        else:
            return None

    def print_menu(self) -> None:
        print('MENU')
        print('1. End your turn')
        print('2. Roll the Dice')
        print('3. Buy a settlement')
        print('4. Buy a city ')
        print('5. Buy a road ')
        print('6. Buy a development card')
        print('8. Play a knight ')
        print('9. Play a road ')
        print('10. Play a plenty')
        print('11. Play mono')
        print('12. Trade')
        print('13. Target ')

    def turn_choice(self, board):
        choice = 0
        # Print the menu
        self.print_menu()

        # Get input - must be a number between 1 and 13
        while choice < 1 or choice > 13:
            try:
                choice = int(input('Enter Choice: \n'))
                if choice < 1 or choice > 13:
                    print('Enter a number between 1 and 13')
            except:
                print('You must input a numeric value between 1 and 13')
        return choice

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
        print('Robber activated!')
        # Get the number of cards to discard. Will be zero if less than 7 cards.
        total = self.resource_cards.get_discard_num()
        if total > 0:
            # Ask player which cards to discard
            offer = self.offer_cards()
            # Make sure the total offer is correct
            while sum(offer.values()) != total:
                print('You must choose exactly {0} cards'.format(total))
                offer = self.offer_cards()
            return offer
        else:
            # If total is 0
            print("You don't have to discard cards now.")
            return None

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
        # print list of resources to choose form 1 -5
        for i in range(len(constants.RESOURCE_NAMES) + 1):
            print(i, constants.RESOURCE_NAMES[i])

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
        try:
            resource_own = int(input('What resource would you like to trade in?'))
            resource_bank = int(input('What resource would you like to receive?'))

            if resource_own == resource_bank:
                print("You can not trade and receive the same resource")
                # return None to go back to main menu
                return None, None
            else:
                # Determine how many cards the player needs to give to the bank
                give = self.ports_trade(resource_own)
                # Ensure the player has those cards
                if self.resource_cards.resource_cards[resource_own] >= give:
                    return resource_own, resource_bank, give
                else:
                    print("You do not have sufficient {} cards to trade in".format(resource_own))
                    return None, None
        except:
            print("Invalid input")
            # give the player another chance for proper input
            return self.trade_bank(self, board)

    def trade_offer(self, board):
        """
        resources_own - what the player is offering
        resources_own_amount - amount of the resource they are offering
        target_player_nr -- integer 0-3
        resources_target and resources_target_amount - what they are willing
        to accept in the trade
        """
        try:
            resource_own = int(input('What resource would you like to trade in?'))
            resource_own_amount = int(input("How many {} would you like to offer"
                                            .format(constants.RESOURCE_NAMES[resource_own])))
            target_player_nr = int(input("Which player would you like to trade with?"))
            resource_target = int(input('What resource would you like to receive?'))
            resource_target_amount = int(input("How many {} would you like to offer"
                                               .format(constants.RESOURCE_NAMES[resource_own])))

            if self.resource_cards.resource_cards[resource_own] >= resource_own_amount:
                return ((resource_own, resource_own_amount),
                        target_player_nr,
                        (resource_target, resource_target_amount))
            else:
                print("You do not have sufficient {} cards to trade in".format(resource_own))
                return self.trade_offer(self, board)

        except:
            print("Invalid input")
            # give the player another chance for proper input
            return self.trade_offer(self, board)

    def trade_answer(self, board, resources_offered, resources_asked):
        print("You have been offered the following trade")
        print("{} {} in exchange for {} {}".format(resources_offered[0],
                                                   resources_offered[1],
                                                   resources_asked[0],
                                                   resources_asked[1]))

        while True:
            try:
                decision = input("Would you like to accept? Y/N")
                if decision == 'y' or decision == 'Y':
                    return True
                elif decision == 'n' or decision == 'N':
                    return False
            except:
                print("Invalid input, try again")
            finally:
                print("Invalid input, try again")

    def get_valid_settlements_start(self, board):
        valid_settlements = []
        # check if the intersection's neighbors are all empty
        for settlement in board.intersections: # board.intersections is a dictionary
            for neighbor in board.intersections[settlement].get_neighbors():
                if neighbor.occupier is not None:
                    break # go to the next settlement
            # if all the neighbors pass the test (is None) add to valid_settlements
            valid_settlements.append(board.intersections[settlement].identifier)

        return valid_settlements

    def get_valid_roads_start(self, board, settlement_position):
        valid_roads = []
        # check if the road is attached to the player's roads
        # and is available (will have to be available bc if not the settlement could not be placed there)
        for road in board.intersections[settlement_position].edges:
            if road.occupier is None:
                valid_roads.append(road.identifier)
        return valid_roads

    def start_settlement_placement(self, board):
        # check for valid_settlements
        valid_settlements = self.get_valid_settlements_start(board)
        # get settlement input
        print("Choose a settlement")
        settlement_position = self.get_index_input(valid_settlements)
        # get valid road
        valid_roads = self.get_valid_roads_start(board, settlement_position)
        # get road input
        print("Choose a road")
        road_position = self.get_index_input(valid_roads)

        # Purchase the road and settlement
        self.purchase_settlement(settlement_position, board, True)
        self.purchase_road(road_position, board, True)

        # Return the two integers
        return settlement_position, road_position


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
    p.start_settlement_placement(b)
    # print(p.resource_cards)
    # p.resource_cards = ResourceCards(4)
    # p.discard_half()

    print('Debug complete')
