
from ctypes import pointer
from utils import toDraw, gameProb, expectedWin


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

    def checkSecondWin(self, dealerPoint):
        if self.secondResult=="BlackJack":
            return "B"
        if self.secondResult==-1:
            return "L"
        if dealerPoint==-1:
            return "W"
        if self.secondResult>dealerPoint:
            return "W"
        elif self.secondResult==dealerPoint:
            return "T"
        else:
            return "L"

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

    def getExpectedValue(self):
        return expectedWin(sum(self.cards), self.hasAce,  self.dealer.getFirst(), self.dealer.getRemaining())

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

    def splittingPairs(self):
        return False
        if self.cards[0]==self.cards[1]:
            dealerFirstCard = self.dealer.getFirst()
            if self.cards[0]==1 or self.cards[0]==8:
                self.executeSplittingPairs()
                return True
            if (self.cards[0]==2 or self.cards[0]==3 or self.cards[0]==7) and (dealerFirstCard<8 and dealerFirstCard!=1):
                self.executeSplittingPairs()
                return True
            if self.cards[0]==6 and (2<=dealerFirstCard<=6):
                self.executeSplittingPairs()
                return True
        return False

    def executeSplittingPairs(self):
        #Get base card and get a card for the first round
        baseCard = self.cards.pop()
        self.cards.append(self.dealer.givePlayerCard())
        # Execute first pair
        if not self.isBlackJack():
            #self.naivePlaying(11)
            self.calculateCardPlaying()
            #self.onlineStrategy()
        self.secondResult = self.result
        # Execute second pair
        self.cards = [baseCard]
        self.cards.append(self.dealer.givePlayerCard())
        if not self.isBlackJack():
            #self.naivePlaying(11)
            self.calculateCardPlaying()
            #self.onlineStrategy()

    def memoryDoubleDown(self):
        summ = sum(self.cards)
        dealerFirstCard = self.dealer.getFirst()
        remainings = self.dealer.getRemaining()
        # Expected win directly get
        origExpected = expectedWin(summ, self.hasAce, dealerFirstCard, remainings)
        print("Double down: ", origExpected, dealerFirstCard, self.cards)
         
        if 9<=summ<=11:
            # Check whether the expected value is positive
            size = float(sum([v for v in remainings.values()]))
            expectedValue = 0
            for i in range(1, 11):
                if remainings[i]==0:
                    continue
                occurProb = remainings[i]/size
                remainings[i] -= 1
                if i==1 and summ+11<=21:
                    expectedValue += occurProb*gameProb(summ+11, dealerFirstCard, remainings)
                else:
                    expectedValue += occurProb*gameProb(summ+i, dealerFirstCard, remainings)
                remainings[i] += 1
            if expectedValue>=0:
                self.executeDoubleDown()
                return True
        return False


    def doubleDown(self):
        summ = sum(self.cards)
        dealerFirstCard = self.dealer.getFirst()

        if 9<= summ <=11:
            if summ==11:
                self.executeDoubleDown()
                return True
            if summ==10 and (dealerFirstCard!=10 or dealerFirstCard!=1):
                self.executeDoubleDown()
                return True
            if summ==9 and (2<=dealerFirstCard<=6):
                self.executeDoubleDown()
                return True
        else:
            return False
    
    def executeDoubleDown(self):
        self.cards.append(self.dealer.givePlayerCard())
        points = sum(self.cards)
        if self.cards[-1]==1:
            self.hasAce = 1
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

    def getDealer(self):
        return self.dealer
            
        

    def reset(self):
        self.cards = []
        self.hasAce = 0
        self.result = "Not initialize"
