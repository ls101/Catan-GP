import random
import constants
import catan

#import the list of development cards - shuffle it so it is random every game 

# create a class for cards and anything card related
class Cards():
    def __init__(self):
      self.cards = []

    def __str__(self):
        cards_iterated = ""
        for card in range(len(self.cards)):
            cards_iterated += "{0}: {1} , ".format(card, self.cards[card])
        return cards_iterated

    def cards_length(self):
        return len(self.cards)

    # see if a certain value is in the deck
    def cards_contain(self,card_test):
        for card in self.cards:
            if card==card_test:
                return True
        return False

    def cards_insert(self, *cards_insert):
        for card in cards_insert:
            self.cards.append(self.cards)

    # this function removes cards
    def cards_remove(self, cards_remove):
        self.cards.remove(cards_remove)

    def last_card(self):
        last=self.cards[-1]
        return last 



""" dev cards are the only cards. Not sure why we need inheritance """
class DevCards(Cards):
    # in order to make sure that a development card is not used in the
    # turn it wasborn instead of the
    # dev card being an instance of the card class
    # i created an inherited class of the sub class ..
    # the index of the dev card will be the same as the card itself
    # when ever you buy a dev card it will reference the turn by index
    # and make sure the turn you bought it is not the
    # turn in which you want to use it
    def __init__(self):
        """ super.__init__(self) -- this is Java syntax """
        Cards.__init__(self)
        self.turn=[]

    def turn_setter(self,turn):
        # when you purchase a dev card you will also set which turn it is
        turn.append(turn)

    def use_dev_card(self,card_choice,game_turn):
        # this method determines if one can use the dev card
        # by seeing which turn they bought it and which turn they are up
        # to in the game
        can_use = False
        index = card_choice - 1
        """ if turn[index]==game_turn: -- must use "self" in Python """
        if self.turn[index] == game_turn:
            print('you can not use a development card on the turn in which you purchased it')
        else:
            can_use = True
        return can_use

    def buy_card(self, turn):
        """
        - add a new card to player list
        - remove that card from game deck
        - ensure this card cannot be used for this turn
        - return the card
        """

        card=catan.bank_devcards.pop()
        self.Cards.cards_insert(card)
        self.turn.turn_setter(turn)
        return card 


    def check_victory(self, card):
        """
        - check if the card is a victory points card
        - return 0 or 1
        """
        last=Cards.last_card(self)
        if last==1:
            return 1
        else:
            return 0
        

    def can_play(self, turns, card_type):
        """
        - card_type refers to the type of development card
        - check that the player has the card
        - check that the card was not bought at this turn
        - check that the player didn't yet play a development card at this turn
        - return a tuple: True or False, and the card
        """
        return (True, 'demo card')  # temporary for debugging

        if card_type not in self.Cards:
            print("you do not have the cards to play this move")
            return False,""
        else:
            card_len=self.Cards.length-1
            index=0
            card=0
            for i in range (card_len,-1,-1):
                if i==card_type:
                    card=self.cards[i]
                    index=i
                    break
            if self.turn[index]==turns:
                print("you cannot play a card on the turn you bought it")
                return False,""
            else:
                return True,card
       

    def return_to_deck(self, card):
        """
        - return a card to the bottom of the deck
        - when a player picks a card, it should NOT be the one last returned
        """
        index=0
        #get the index to remove turn 
        for i in self.Cards:
            if i==card:
                index=i
                break
        
        self.Cards.cards_remove(card)
        self.catan.bank_devcards.insert(0,card)
        self.turn.pop(index)





# The resource cards should rather be stored as a dictionary. The resources
# will be keys, mapped to the amount (number) of that card type owned by the
# object. This object will be initialized for each player, as well as one
# for the bank.
class ResourceCards:
    # Ideally, the RESOURCE_NAMES list should be coded ONCE for the entire game
    # and then imported. It is here temporarily.
    # Note: dessert was removed from this list.
    RESOURCE_NAMES = constants.RESOURCE_NAMES

    def __init__(self, num=0):
        # The object is initialized with a dictionary as mentioned above.  The
        # players start with no cards; the bank starts with 19 of each.
        self.resource_cards = {}
        for item in self.RESOURCE_NAMES:
            if item != "desert":
                self.resource_cards[item] = num

    def __str__(self):
        if self.get_total_cards() == 0:
            return 'You have no resource cards.'
        s = 'You have:\n'
        for key, value in self.resource_cards.items():
            if value > 0:
                s += '{0} {1}\n'.format(value, key)
        return s

    def get_total_cards(self):
        return sum(self.resource_cards.values())

    def get_discard_num(self):
        # when the robber is activated, all players who have more than seven
        # cards need to discard half. (Those will be returned to the bank.)
        # For odd numbers, we round down. I used integer division to get a
        # whole number.
        total = self.get_total_cards()
        if total <= 7:
            discard = 0
        else:
            discard = total//2
        return discard

    def move_cards(self, other, what):
        # For receiving cards from the bank, or for trading:
        # "self" (the object that calls the method) is RECEIVING cards from
        # "other".  For receiving new cards, other refers to the bank, which
        # will need to  be an object. "what" refers to which cards are moved,
        # and should be in a dictionary format.
        s = self.resource_cards
        o = other.resource_cards
        for key, value in what.items():
            s[key] += value
            o[key] -= value

    def get_random_card(self):
        # For choosing a random card to steal. The actual stealing should
        # be done on the dictionary.

        # Create a local list, to enable choosing a random card.
        lis = []
        for key, value in self.resource_cards.items():
            lis += [key] * value
        # Get a random card
        card = random.choice(lis)
        # return the card in dictionary format, to be used in the
        # move_cards method
        return {card: 1}
   


if __name__ == '__main__':
    pass


