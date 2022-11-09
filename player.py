
from utils import toDraw


class Player:
    def __init__(self, id, dealer):
        self.id = id
        self.cards = []
        self.dealer = dealer
        self.hasAce = 0
        self.result = "Not initialize"

    def printCards(self):
        print("Player ", self.id , "cards:", self.cards, "result", self.result)

    def isBlackJack(self):
        assert len(self.cards)==2, "Dummy blackJacke call, # of dealer's cards != 2"
        if self.cards[0]+self.cards[1]==11:
            if self.cards[0]==1 or self.cards[1]==1:
                self.result = "BlackJack"
                return True
        return False

    def recievedCard(self, card):
        self.cards.append(card)
        if card==1:
            self.hasAce = 1

    def checkWin(self, dealerPoint):
        if self.result=="BlackJack":
            return "B"
        if self.result==-1:
            return "L"
        if dealerPoint==-1:
            return "W"
        if self.result>dealerPoint:
            return "W"
        elif self.result==dealerPoint:
            return "T"
        else:
            return "L"

    def naivePlaying(self, thresHold=17):
        points = sum(self.cards)
        while points<thresHold and (points+10*self.hasAce<thresHold or points+10*self.hasAce>21):
            self.cards.append(self.dealer.givePlayerCard())
            if self.cards[-1]==1:
                self.hasAce = 1
            points += self.cards[-1]
        if points > 21:
            self.result = -1
        else:
            if points+10*self.hasAce<=21:
                self.result =  points+10*self.hasAce
            else:
                self.result =  points

    

    def naivePlayingWithSoftHand(self, thresHold=17):
        points = sum(self.cards)
        while (points<thresHold and (points+10*self.hasAce<thresHold or points+10*self.hasAce>21)) or (self.hasAce==1 and points+10*self.hasAce<18):
            self.cards.append(self.dealer.givePlayerCard())
            if self.cards[-1]==1:
                self.hasAce = 1
            points += self.cards[-1]
        if points > 21:
            self.result = -1
        else:
            if points+10*self.hasAce<=21:
                self.result =  points+10*self.hasAce
            else:
                self.result =  points
    
    def onlineStrategy(self):
        firstCard = self.dealer.getFirst()
        if firstCard==1 or firstCard>7:# If dealer has a good one, not stop until reach 17
            self.naivePlayingWithSoftHand(17)
        elif firstCard>3: # Dealer has poor card(4, 5, 6), not stop until reach 12
            self.naivePlayingWithSoftHand(12)
        else: # Dealer has poor card(2, 3), not stop until reach 13
            self.naivePlayingWithSoftHand(13)


    def calculateCardPlaying(self):
        points = sum(self.cards)
        while toDraw(points, self.hasAce, self.dealer.getFirst(), self.dealer.getRemaining()):
            self.cards.append(self.dealer.givePlayerCard())
            if self.cards[-1]==1:
                self.hasAce = 1
            points += self.cards[-1]
            if points>21:
                break
        if points > 21:
            self.result = -1
        else:
            if points+10*self.hasAce<=21:
                self.result =  points+10*self.hasAce
            else:
                self.result =  points
            
        

    def reset(self):
        self.cards = []
        self.hasAce = 0
        self.result = "Not initialize"
