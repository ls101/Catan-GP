import numpy as np
import random
from board import Board
import cards
import player
import constants
import visual

RESOURCE_NAMES = constants.RESOURCE_NAMES
DEVELOPMENT_CARD_NAMES = constants.DEVELOPMENT_CARD_NAMES
PRICES = constants.PRICES
PLAYER_COLORS = constants.PLAYER_COLORS
dev_dict = dict(zip(DEVELOPMENT_CARD_NAMES,np.arange(0, len(DEVELOPMENT_CARD_NAMES))))


class CatanBoard:
    # Initialize the Catan Board with all the options for resources, numbers to
    # be rolled, settlements/roads, port options
    def __init__(self):
        self.board = Board()
        self.bank = cards.ResourceCards(19)

        # get a GUI
        self.gui = visual.GUIboard(self.board)

        # insert players
        self.players = list()
        for player_nr in range(constants.NUM_PLAYERS):
            self.players.append(player.CatanPlayer(player_nr))

        # player_points player0, player1, player2, player3
        self.player_points = [0, 0, 0, 0]
        # longest road player_number. Initialization with -1.
        self.longest_road = -1
        # longest largest_army player_number. Initialization with -1.
        self.largest_army = -1
        # devcards according to dev_dict dictionary
        self.bank_devcards = np.array([
            14*[dev_dict["knight"]]
            + 5*[dev_dict["victory point"]]
            + 2*[dev_dict["road building"]]
            + 2*[dev_dict["year of plenty"]]
            + 2*[dev_dict["monopoly"]]
        ])
        np.random.shuffle(self.bank_devcards)
        # played open knight cards for each player
        self.open_knights = [0, 0, 0, 0]

        """ -- update this from DevCards class -- """
        # hidden unplayed dev cards for each player
        # as 2d matrix  dev_dict x  player_nr
        self.hidden_dev_cards = np.array([[0]*5]*4)
        # how many dev cards were just bought this turn and can not be played
        # as 2d matrix dev_dict x  player_nr
        self.new_hidden_dev_card = np.array([[0]*5]*4)

    # String output for printing the board
    def __str__(self):
        return str(self.board)

    def check_longest_road(self):
        pass

    def check_largest_army(self):
        pass

    def get_resources(self, dice_number):
        """ check if the bank has it """
        for cur_player in self.players:
            # For each player, check if they have resources with the number
            # of the dice rolled.
            c = {}  # initialize a dict
            for i in cur_player.resources:
                if i[0] == dice_number:
                    key = RESOURCE_NAMES[i[1]]  # The key for the dict
                    # For each resource, check if there is such a key.
                    # Meaning, if the player has more than one of a given
                    # resource, increment it. Otherwise, add it.
                    c[key] = c.get(key, 0) + 1
                # the player receives cards from the bank.
                cur_player.resource_cards.move_cards(self.bank, c)

    def place_road(self, player_nr, position):
        # Reassign the road's occupier
        self.board.edges[position].occupier = \
            PLAYER_COLORS[player_nr] + " player's road"
        print(self.board.edges[position])
        self.gui.buy_road(player_nr, position)

    def place_settlment(self, player_nr, position):
        # buy the settlement: reassign the intersection's occupier and
        # update the gui.
        # The rest is done in the player class
        self.board.intersections[position].occupier = (
            player_nr, PLAYER_COLORS[player_nr] + " player's settlement")
        print(self.board.intersections[position])
        self.gui.buy_settlement(player_nr, position)
        # Update the points for the player
        self.player_points[player_nr] += 1

        # Mark the neighboring intersections as restricted - cannot have
        # a settlement.
        for i in self.board.intersections[position].get_neighbors():
            i.occupier = (-1, 'restricted')
            self.gui.restrict_edge(i.identifier)
            print(i)

    def start_settelment_first(self, player_nr, settle_position, road_position):
        # Place the road
        self.place_road(player_nr, road_position)
        # Place the settlement
        self.place_settlment(player_nr, settle_position)

    def start_settelment_second(self, player_nr, settle_position, road_position):
        # Set the settlement and road
        self.start_settelment_first(player_nr, settle_position, road_position)
        # Give the resource cards to the player.
        c = {}  # initialize a dict
        for i in self.board.intersections[settle_position].terrains:
            key = RESOURCE_NAMES[i.resource]  # The key for the dict
            # If the resource is not desert, check if there is such a key.
            # Meaning, if there are more than one neighboring terrain with
            # the same resource.
            if key != 'desert':
                c[key] = c.get(key, 0) + 1
        # the player receives cards from the bank.
        self.players[player_nr].resource_cards.move_cards(self.bank, c)
        print(c)

    def check_points(self):
        """
        output --
        game_end (logical)
        winner (integer 0-3)
        """
        game_end, winner = False, 0
        return game_end, winner

    def buy_settlement(self, player_nr, position):
        # pay for the settlement
        self.bank.move_cards(self.players[player_nr].resource_cards, PRICES['settlement'])
        # place the settlement (and update points)
        self.place_settlment(player_nr, position)

    def buy_city(self, player_nr, position):
        # pay for the city
        self.bank.move_cards(self.players[player_nr].resource_cards, PRICES['city'])
        # buy the city: reassign the settlement's occupier and update the gui.
        # The rest is done in the player class
        self.board.intersections[position].occupier = (
            player_nr, PLAYER_COLORS[player_nr] + " player's city")
        print(self.board.intersections[position])
        self.gui.buy_city(player_nr, position)
        # Update the points for the player
        self.player_points[player_nr] += 1

    def buy_road(self, player_nr, position):
        # pay for the road
        self.bank.move_cards(self.players[player_nr].resource_cards, PRICES['road'])
        # buy the road:
        self.place_road(player_nr, position)
        # Check length
        self.check_longest_road()

    def buy_dev_card(self, turns, player_nr,):
        cur_player = self.players[player_nr]
        # Check if player has enough resources to buy the card
        if not player.can_buy('dev_card'):
            print('You do not have the required resources to buy a development card.')
        else:
            # pay for the card
            self.bank.move_cards(cur_player.resource_cards, PRICES['dev_card'])
            # buy the card
            card = cur_player.development_cards.buy_card(turns)
            if cur_player.development_cards.buy_card(card):
                self.player_points[player_nr] += 1
            print('Card purchased successfully.')

    def roll(self):
        min = 1
        max = 6
        value = random.randint(min, max)
        return value

    def roll_dice(self):
        dye1 = self.roll()
        dye2 = self.roll()
        dice_values = dye1+dye2
        return dice_values

    def discard_half(self, player_nr, resources):
        # The bank is receiving half of the player's cards. "resources" refers
        # to the cards that the player chose to discard.
        self.bank.move_cards(self.players[player_nr].resource_cards, resources)

    def steal_card(self, player_nr, position, target_player_nr):
        # Update the robber position
        self.board.robber = position
        # Check if target player has any cards
        if self.players[target_player_nr].resource_cards.get_total_cards() == 0:
            print("Sorry, your target doesn't have any cards")
        else:
            # Get a random card and move it to the player who plays robber.
            steal = self.players[target_player_nr].resource_cards.get_random_card()
            self.players[player_nr].resource_cards.move_cards(
                self.players[target_player_nr].resource_cards, steal)

    def play_knight(self, turns, player_nr, position, target_player_nr):
        cur_player = self.players[player_nr]
        can_play, card = cur_player.development_cards.can_play(turns, 'knight')
        if can_play:
            self.steal_card(player_nr, position, target_player_nr)
            # return the card to the game deck
            cur_player.development_cards.return_to_deck(card)
            # Update the army
            cur_player.army += 1
            self.open_knights[player_nr] += 1
            self.check_largest_army()

    def play_roads(self, turns,  player_nr, position1, position2):
        cur_player = self.players[player_nr]
        can_play, card = cur_player.development_cards.can_play(turns, 'road building')
        if can_play:
            # Place the roads: reassign the road's occupier and update the gui.
            # The rest is done in the player class
            self.place_road(player_nr, position1)
            self.place_road(player_nr, position2)
            # return the card to the game deck
            cur_player.development_cards.return_to_deck(card)
            # Check length
            self.check_longest_road()

    def play_plenty(self, turns, player_nr, resource1, resource2):
        cur_player = self.players[player_nr]
        can_play, card = cur_player.development_cards.can_play(turns, 'year of plenty')
        if can_play:
            # Initialize a dict with resource1
            c = {constants.RESOURCE_NAMES[resource1]: 1}
            # Add resource2; ensure it's added even if both are the same
            c[constants.RESOURCE_NAMES[resource2]] = c.get(constants.RESOURCE_NAMES[resource2], 0) + 1
            """ check if the bank has it """
            # The player receives cards from the bank.
            cur_player.resource_cards.move_cards(self.bank, c)
            # return the card to the game deck
            cur_player.development_cards.return_to_deck(card)

    def play_mono(self, turns, player_nr, resource):
        cur_player = self.players[player_nr]
        can_play, card = cur_player.development_cards.can_play(turns, 'monopoly')
        if can_play:
            # Initialize a counter
            cards = 0
            # Add everyone's cards of that resource type, and remove from
            # that player.
            for player_nr in self.players:
                cards += player_nr.resource_cards.resource_cards[constants.RESOURCE_NAMES[resource]]
                player_nr.resource_cards.resource_cards[constants.RESOURCE_NAMES[resource]] = 0

            # Add those cards to the player who plays now
            cur_player.resource_cards.resource_cards[resource] = cards
            # return the card to the game deck
            cur_player.development_cards.return_to_deck(card)

    def trade_bank(self, player_nr, resource_own, resource_bank, give):
        # Check that the bank has the card
        if self.bank.resource_cards[resource_bank] >= 1:
            # Create the dictionary for the move_cards method.
            # Since it's done in one call, the cards given are negative.
            d = {
                constants.RESOURCE_NAMES[resource_bank]: 1,
                constants.RESOURCE_NAMES[resource_own]: -give
            }
            self.players[player_nr].resource_cards.move_cards(self.bank, d)
        else:
            print('Sorry, the bank does not have the requested resource')

    def trade_offer(
        self,
        player_nr,
        resource_own,
        resource_own_amount,
        target_player_nr,
        resource_target,
        resource_target_amount
    ):
        d = {
                constants.RESOURCE_NAMES[resource_target]: resource_target_amount,
                constants.RESOURCE_NAMES[resource_own]: -resource_own_amount
            }
        self.players[player_nr].resource_cards.move_cards(
            self.players[target_player_nr], d)



if __name__ == '__main__':
    b = CatanBoard()

    b.gui.window.mainloop()
    print('Debug complete')
