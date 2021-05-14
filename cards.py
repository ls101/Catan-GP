#create a class for cards and anything card related 
class cards():
    def __init__(self,player):
      self.player=player
      self.cards=[]

    def __str__(self):
       cards_iterated=""
       for card in cards :
           cards_iterated+=card
       return cards_iterated
    
    def cards_length(self):
        return len(self.cards)
    
    # see if a certain value is in the deck 
    def cards_contain(self,card_test):
        for card in self.cards:
            if card==card_test:
                return True
        return False
