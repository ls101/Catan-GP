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
        self.resource_cards = ResourceCards()
        self.development_cards = Cards()
        
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
            return self.get_input_by_index(lis)
        # Otherwise, validate the input data: must be a digit, and a  valid
        # index for this list.
        elif not position.isdigit():
            print('Input must be an integer. Please try again.')
            return self.get_input_by_index(lis)
        elif not 0 < int(position) < len(lis):
            print('Input must be greater than zero and less than {0}. Please try again'.format(len(lis)))
            return self.get_input_by_index(lis)
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
            return self.get_input_by_value(lis)
        # Otherwise, validate the input data: must be a digit, and an integer
        # that is in this list.
        elif not position.isdigit():
            print('Input must be an integer. Please try again.')
            return self.get_input_by_value(lis)
        elif not int(position) in lis:
            print('Your chosen number is not in the list. Please try again.')
            return self.get_input_by_value(lis)
        else:
            return int(position)

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


    def can_buy(self, dict):
        # The dict refers to whatever the player wants to buy. It is whether
        # the price of a settlement/city/development card/road. The dict can
        # also refer to cards that the player wants to trade away.
        for key, value in dict.items():
            # If the player wants to give more than s/he has, it returns false.
            # If it exits the loop without raising a flag, it returns true.
            if value > self.resource_cards.resource_cards[key]:
                return False
            return True




if __name__ == '__main__':
    
    p = CatanPlayer(0)
    print(p.player_nr)
    # print(p.discard_half())
    # test_list = [10,20,30,40,50]
    # p.get_input_by_index(test_list)
    # p.get_input_by_value(test_list)
    print('Debug complete')
