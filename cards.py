#create a class for cards and anything card related 
class Cards():
    def __init__(self,player):
      self.player=player
      self.cards=[]

    def __str__(self):
       cards_iterated=""
       for card in cards :
           cards_iterated+=" ,"+card
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
            


player1_cards=str(Cards())
player2_cards=str(Cards())
player3_cards=str(Cards())
player4_cards=str(Cards())

#this class will can contain a dictionary with objects of cards all the players 
#this will corespond to players... for easy reference 
class AllCards(self):
    def __init__(self):
        self.card_store={
            0:player1_cards,
            1:player2_cards,
            2:player3_cards,
            3:player4_cards
        }

       

