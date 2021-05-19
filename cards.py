#create a class for cards and anything card related 
class Cards():
    def __init__(self):
      self.cards=[]

    def __str__(self):
       cards_iterated=""
       for card in range(len(self.cards)):
           cards_iterated+="{0}: {1} , ".format(card, self.cards[card])
       return cards_iterated
    

    def cards_length(self):
        return len(self.cards)
    
    # see if a certain value is in the deck 
    def cards_contain(self,card_test):
        for card in self.cards:
            if card==card_test:
                return True
        return False
    
    def cards_insert(self,*cards_insert):
        for card in cards_insert:
         self.cards.append(cards)
    
    #this function removes cards
    def cards_remove(self,*cards_remove):
        pass
            



# The resource cards should rather be stored as a dictionary. The resources
# will be keys, mapped to the (num) ber of that card type owned by the object.
# This object will be initialized for each player, as well as one for the bank.
class ResourceCards:
    # Ideally, the RESOURCE_NAMES list should be coded ONCE for the entire game
    # and then imported. It is here temporarily.
    # Note: dessert was removed from this list.
    RESOURCE_NAMES = ["brick", "ore", "hay", "wood", "sheep"]

    def __init__(self, num=0):
        # The object is initialized with a dictionary as mentioned above.  The
        # players start with no cards; the bank starts with 19 of each.
        self.resource_cards = {}
        for item in self.RESOURCE_NAMES:
            self.resource_cards[item] = num 

    def __str__(self):
        if self.get_total_cards() == 0:
            return 'You have no resource cards.'
        s = 'You have:\n'
        for key, value in self.resource_cards.items():
            if value > 0:
                s += str(value) + ' ' + key + '\n'
        return s

    def get_total_cards(self):
        return sum(self.resource_cards.values())

    def get_discard_num(self):
        # when the robber is activated, all players who have more than seven
        # cards need to discard half. (Those will be returned to the bank.)
        # For odd numbers, we round down. I used integer division to get a whole number.
        total = self.get_total_cards()
        if total <= 7:
            discard = 0
        else:
            discard = total//2
        return discard

    def move_cards(self, other, what):
        # For receiving cards from the bank, or for trading:
        # "self" (the object that calls the method) is RECEIVING cards from "other".
        # For receiving new cards, other refers to the bank, which will need to
        # be an object. "what" refers to which cards are moved, and should be
        # in a dictionary format.
        s = self.resource_cards
        o = other.resource_cards
        for key, value in what.items():
            s[key] += value
            o[key] -= value

    def resources_list(self):
        # For operations that work better on list objects, such as choosing a
        # random card to steal. The actual stealing should be done on the dictionary.
        lis = []
        for key, value in self.resource_cards.items():
            lis += [key] * value
            # for x in range(value):
            #     lis.append(key)
        return lis



""" 
These should be initialized from the player class, as it belongs to the player
player1_cards=str(Cards())
player2_cards=str(Cards())
player3_cards=str(Cards())
player4_cards=str(Cards())
 """

""" #this class will can contain a dictionary with objects of cards all the players 
#this will corespond to players... for easy reference 
class AllCards(self):
    def __init__(self):
        self.card_store={
            0:player1_cards,
            1:player2_cards,
            2:player3_cards,
            3:player4_cards
        } """

if __name__ == '__main__':
    c = ResourceCards()
    d = ResourceCards(19)
    cc = Cards()
print(cc)       