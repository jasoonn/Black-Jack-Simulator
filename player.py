
from curses.ascii import isblank


class Player:
    def __init__(self, id, dealer):
        self.id = id
        self.cards = []
        self.dealer = dealer
        self.hasAce = 0

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
        if self.result==22:
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

    # Start the game with specific drawing strategy
    def startPlaying(self, strategy):
        if self.isBlackJack():
            self.result = 22
        else:
            self.result = sum(self.cards)
            #self.result = strategy(sum(self.cards), 1 in self.cards, self.dealer)

    def naivePlaying(self, thresHold=17):
        if self.isBlackJack():
            return
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

    def reset(self):
        self.cards = []
        self.hasAce = 0
        self.result = "Not initialize"
