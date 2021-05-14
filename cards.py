#create a class for cards and anything card related 
class Cards():
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
    
    def cards_insert(self,*cards):
        for card in cards:
         self.cards.append(cards)
    
    #this function removes cards
    def cards_remove(self,*cards):
        pass


player1_cards=Cards()
player2_cards=Cards()
player3_cards=Cards()
player4_cards=Cards()

#this class will can contain a dictionary with objects of cards all the players 
#this will corespond to players... for easy reference 
class AllCards(self):
    def __init__(self):
        self.card_store={}

       

