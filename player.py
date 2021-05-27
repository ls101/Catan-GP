from board_components import RESOURCE_NAMES
import numpy as np
from cards import *
import constants
# import board as board

prices = constants.PRICES


class CatanPlayer:
    # Initialize the Catan Board with all the options for resources, numbers
    # to be rolled, settlements/roads, port options
    def __init__(self, player_nr):
        self.player_nr = player_nr
        self.unused_items = {
            'roads': 15,
            'settlements': 5,
            'cities': 4
        }
        # Items placed on the board will be an array containing the index
        # numbers of those items, which are stored in arrays. The index
        # numbers match the numbers on the diagram.
        self.roads = []
        self.settlements = []
        # Note that cities are added by removing said item from the
        # settlements list
        self.cities = []
        # port where the player has a settlement
        self.ports = []

        # All items owned by the player, but not on the board:
        # self.resource_cards = ResourceCards(4)  # for debugging
        self.resource_cards = ResourceCards()
        self.development_cards = DevCards()

        # Game statistics, regarding this player:
        # self.road_length = 0
        self.army = 0
        self.victory_points = 0

        # Resources that correspond to where the player has
        # settlements/cities - double resources for cities
        # It is stored as a tuple - (resource_num, resource_type)
        self.resources = []

    # Find valid locations for settlements based on current settlements
    # and roads - the new settlement must be attached to the player's
    # road and occupier must be None
    def get_valid_settlements(self, board):
        valid_settlements = []
        # check if the intersection attached to the player's roads
        # is available
        for road in self.roads:
            for intersection in board.edges[road].intersections:
                if intersection.occupier is None:
                    valid_settlements.append(intersection.identifier)
        return set(valid_settlements)

    def get_valid_roads(self, board, position1=None):
        valid_roads = []
        # check if the road is attached to the player's roads
        # and is available
        for road in self.roads:
            for neighbor in board.edges[road].get_neighbors():
                if neighbor.occupier is None:
                    valid_roads.append(neighbor.identifier)
        # Position for adding two roads (development card) Remove the first
        # road added for can not be added a second time
        if position1 is not None:
            valid_roads.remove(position1)
        return set(valid_roads)

    # Takes a list of valid positions to place object and asks for input
    # If the input is valid, returns the position
    # Otherwise the player can try again
    def get_index_input(self, valid_positions):
        print(valid_positions)
        while True:
            try:
                position = int(input("Choose a position(number) from the list"))
            except:
                print("Invalid input, try again")
            else:
                if position in valid_positions:
                    return position
                else:
                    print("Invalid choice, try again")

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
        if not type_to_buy == 'dev_card' and self.unused_items[type_to_buy] <= 0 :
            # Player has a limit on roads, settlements, cities.
            return False
        return True

    def purchase_settlement(self, position, board, override):
        # Add the position to the players list of settlements
        self.settlements.append(position)

        # Add the resources for where the settlement is places
        for terrain in board.intersections[position].terrains:
            self.resources.append((terrain.resource_num, terrain.resource))

        # Add ports - if the intersection has a port, add it to player's ports
        if board.intersections[position].port is not None:
            self.ports.append(board.intersections[position].port)

        # Add point for building settlement
        self.victory_points += 1
        # Remove settlement from unused items
        self.unused_items['settlements'] -= 1

    def purchase_city(self, position, board):
        # Remove the position from settlement and add to cities
        for i in self.settlements:
            if i == position:
                self.settlements.remove(i)
        self.cities.append(position)
        # Add the resources for where the city is places
        for terrain in board.intersections[position].terrains:
            self.resources.append((terrain.resource_num, terrain.resource))

        # Add two points for building a city
        self.victory_points += 2
        # Remove city from unused and put back settlement
        self.unused_items['cities'] -= 1
        self.unused_items['settlements'] += 1

    def purchase_road(self, position, board, override):
        # Add the position to the players list of road
        self.roads.append(position)
        # Remove resource cards that were needed to purchase road

        # Remove road from unused
        self.unused_items['roads'] -= 1

    # Find valid locations for settlements based on current settlements
    # and roads - the new settlement must be attached to the player's
    # road and occupier must be None
    # Override used for first settlements when no resource cards are taken
    def set_settlement(self, board, override=False):
        # check if player has resources to buy settlement
        if self.can_buy('settlements') or override:
            # find valid places to put settlements
            valid_settlements = self.get_valid_settlements(board)

            # Return None for empty list - "return" will exit the method
            if len(valid_settlements) == 0:
                print('You do not have any roads near available intersection.')
                return None
            # print list of valid settlements to choose from to build on
            print(valid_settlements)
            # get a valid position to place the settlement
            position = self.get_index_input(valid_settlements)
            # Purchase the settlement and trade in cards
            self.purchase_settlement(position, board, override)
            return position
        else:
            print('You do not have the required resources to buy a settlement.')
            return None

    def set_city(self, board):
        # check if player has resources to buy city
        if self.can_buy('cities'):
            # find valid places to put cities
            valid_cities = []
            for settlement in self.settlements:
                valid_cities.append(settlement)

            # Return None for empty list - "return" will exit the method
            if len(valid_cities) == 0:
                print('You do not have where to place a city.')
                return None
            # print list of valid cities to choose from to build on
            print(valid_cities)
            # get a valid position to place the city
            position = self.get_index_input(valid_cities)
            # Purchase the city and trade in cards
            self.purchase_city(position, board)
            return position
        else:
            print('You do not have the required resources to buy a city.')
            return None

    def set_road(self, board, override=False, position1=None):
        # check if player has resources to buy settlement
        if self.can_buy('roads') or override:
            # find valid places to put settlements
            valid_roads = self.get_valid_roads(board, position1)

            # Return None for empty list - "return" will exit the method
            if len(valid_roads) == 0:
                print('You do not have any roads near available intersection.')
                return None
            # print list of valid roads to choose from to build on
            # print(valid_roads)
            # get a valid position to place the road
            position = self.get_index_input(valid_roads)
            # Purchase the road and trade in cards
            self.purchase_road(position, board, override)
            return position
        else:
            print('You do not have the required resources to buy a road.')
            return None

    def print_menu(self) -> None:
        print('MENU')
        print('0. End your turn')
        print('1. Buy a Settlement')
        print('2. Buy a City ')
        print('3. Buy a Road ')
        print('4. Buy a Development Card')
        print('5. Play a Knight ')
        print('6. Play a Road ')
        print('7. Play a Plenty')
        print('8. Play Mono')
        print('9. Trade Cards with Bank')
        print('10. Trade Cards with a Player')

    def turn_choice(self, board):
        choice = 42
        # Print the menu
        self.print_menu()

        # Get input - must be a number less than 13
        # (zero or lower ends the turn)
        while choice > 13:
            try:
                choice = int(input('Enter Choice: \n'))
                if choice > 13:
                    print('Enter a number between 0 and 13')
            except:
                print('You must input a numeric value between 0 and 13')
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

    def discard_half(self, player_nr):
        # Get the number of cards to discard. Will be zero if less than 7 cards.
        total = self.resource_cards.get_discard_num()
        if total > 0:
            print('Player #{} - {}: needs to discard cards'.format(
                    player_nr, constants.PLAYER_COLORS[player_nr]))
            # Ask player which cards to discard
            offer = self.offer_cards()
            # Make sure the total offer is correct
            while sum(offer.values()) != total:
                print('You must choose exactly {0} cards'.format(total))
                offer = self.offer_cards()
            return offer
        else:
            # If total is 0
            print('Player #{} - {}: does not need to discard cards now'.format(
                    player_nr, constants.PLAYER_COLORS[player_nr]))
            print("You don't have to discard cards now.")
            return None

    def steal_card(self, board):
        # move the robber to a new tile (int between 1-19), not the current
        # place. Find who has settlements on that tile (return None if none)
        # If occupier is not None and occupier[0] > 0 and not self.player_nr
        # Give list of available players to target (if more than one)
        # Return target player

        # get tile to move robber to
        list_without_robber = list(range(1, 20))
        list_without_robber.remove(board.robber)
        position = self.get_index_input(list_without_robber)
        # find all the players that have a settlement/city on that tile
        affected_players = []

        for intersection in board.terrains[position].intersections:
            if intersection.occupier is not None and intersection.occupier[0] >= 0:
                if not intersection.occupier[0] == self.player_nr:
                    affected_players.append(intersection.occupier[0])

        # Return none if no players have settlements on that tile
        if len(affected_players) == 0:
            print('No one to steal from on this tile.')
            return None
        # Return the one player if only one player has settlements on that tile
        # Convert to set to remove duplicate players
        if len(set(affected_players)) == 1:
            return position, affected_players[0]

        # Let player choose who to target if there is more than one player on the tile
        print('You can now choose which player to rob.')
        target_player = self.get_index_input(list(set(affected_players)))
        return position, target_player

    def play_roads(self, board):
        # Development card gives two roads without resources (override)
        # Purchase road twice and return both positions
        print("Road #1")
        position1 = self.set_road(board, True)
        print("Road #2")
        position2 = self.set_road(board, True, position1)

        return position1, position2

    def play_plenty(self, board):
        # player chooses two resources from the bank
        # return those two numbers
        string_output = "" 
        for index in range(1, len(constants.RESOURCE_NAMES)):
            string_output += "{}-{} ".format(index, constants.RESOURCE_NAMES[index])
        print("Choose a resource")
        print(string_output)
        resource1 = self.get_index_input(list(range(1, 6)))
        resource2 = self.get_index_input(list(range(1, 6)))

        return resource1, resource2

    def play_mono(self, board):
        # choose one resource to take from other players
        # return the number
        string_output = ""
        for index in range(1, 6):
            string_output += "{}-{} ".format(index, constants.RESOURCE_NAMES[index])
        print("Which resource would you like to take from the players? ")
        print(string_output)
        resource = self.get_index_input(list(range(1, 6)))

        return resource

    def ports_trade(self, resource_index):
        # Checks if a player has a port; this allows better trading terms
        # when trading with the bank.
        if resource_index in self.ports:
            return 2
        elif 0 in self.ports:
            return 3
        else:
            return 4

    def trade_bank(self, board):
        """
        There is some duplication here and in the next method.  May be better
        in a separate method.  This was done after 50+ hours of work, goal
        is the program should not crash.
        """
        # print list of resources to choose form 1 -5
        print(self.resource_cards)
        print(constants.RESOURCES_PRINT)
        try:
            resource_own = int(input('What resource would you like to trade in?'))
            if not 1 <= resource_own <= 5:
                print('Invalid resource number. please try again.')
                return self.trade_bank(board)
            resource_bank = int(input('What resource would you like to receive?'))
            if not 1 <= resource_bank <= 5:
                print('Invalid resource number. please try again.')
                return self.trade_bank(board)

        except:
            print("Invalid input")
            # give the player another chance for proper input
            return self.trade_bank(board)

        else:
            if resource_own == resource_bank:
                print("You can not trade and receive the same resource")
                # return None to go back to main menu
                return None
            else:
                # Determine how many cards the player needs to give to the bank
                give = self.ports_trade(resource_own)
                # Ensure the player has those cards
                if self.resource_cards.resource_cards[
                        constants.RESOURCE_NAMES[resource_own]] >= give:
                    return resource_own, resource_bank, give
                else:
                    print("You do not have sufficient {} cards to trade in".format(
                        constants.RESOURCE_NAMES[resource_own]))
                    return None

    def trade_offer(self, board):
        # resources_own - what the player is offering
        # resources_own_amount - amount of the resource they are offering
        # target_player_nr -- integer 0-3
        # resources_target and resources_target_amount - what they are willing
        # to accept in the trade

        print(self.resource_cards)
        print(constants.RESOURCES_PRINT)
        try:
            resource_own = int(input('What resource would you like to trade in?'))
            if not 1 <= resource_own <= 5:
                print('Invalid resource number. please try again.')
                return self.trade_offer(board)

            resource_own_amount = int(input(
                "How many {} would you like to offer".format(
                    constants.RESOURCE_NAMES[resource_own])))

            target_player_nr = int(input("Which player would you like to trade with?"))
            if not 0 <= target_player_nr < constants.NUM_PLAYERS:
                print('Invalid player number. please try again.')
                return self.trade_offer(board)

            resource_target = int(input('What resource would you like to receive?'))
            if not 1 <= resource_target <= 5:
                print('Invalid resource number. please try again.')
                return self.trade_offer(board)

            resource_target_amount = int(input(
                "How many {} would you like to receive".format(
                    constants.RESOURCE_NAMES[resource_target])))

        except:
            print("Invalid input")
            # give the player another chance for proper input
            return self.trade_offer(board)
        else:
            if target_player_nr == self.player_nr:
                print('You cannot trade with yourself.')
                # return None to go back to main menu
                return None
            elif resource_own == resource_target:
                print("You can not trade and receive the same resource")
                # return None to go back to main menu
                return None
            elif self.resource_cards.resource_cards[constants.RESOURCE_NAMES[
                    resource_own]] >= resource_own_amount:
                return (
                    resource_own,
                    resource_own_amount,
                    target_player_nr,
                    resource_target,
                    resource_target_amount
                )
            else:
                print("You do not have sufficient {} cards to trade in".format(
                    constants.RESOURCE_NAMES[resource_own]))
                return None

    def trade_answer(self, board, response_tuple):
        print("You have been offered the following trade")
        print("{0} {1} in exchange for {2} {3}".format(
            response_tuple[1],
            constants.RESOURCE_NAMES[response_tuple[0]],
            response_tuple[4],
            constants.RESOURCE_NAMES[response_tuple[3]]
        ))

        while True:
            try:
                decision = input("Would you like to accept? Y/N")
                if decision == 'y' or decision == 'Y':
                    return True
                elif decision == 'n' or decision == 'N':
                    return False
            except:
                print("Invalid input, try again")

    def get_valid_settlements_start(self, board):
        valid_settlements = []
        # check if the intersection's neighbors are all empty
        for settlement in board.intersections: # board.intersections is a dictionary
            if board.intersections[settlement].occupier is None:
                valid_settlements.append(board.intersections[settlement].identifier)
        return valid_settlements

    def get_valid_roads_start(self, board, settlement_position):
        valid_roads = []
        # check if the road is attached to the player's roads
        # and is available (will have to be available bc if not the settlement
        # could not be placed there)
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

    print('Debug complete')
