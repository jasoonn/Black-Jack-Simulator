
from ctypes import pointer
from utils import toDraw, expectedWin, expectedDoubleDown, oneCardExpected


class Player:
    def __init__(self, id, dealer, splitStrategy, doubleStrategy, drawingStrategy):
        self.id = id
        self.cards = []
        self.dealer = dealer
        self.hasAce = 0
        self.splitStrategy = splitStrategy
        self.doubleStrategy = doubleStrategy
        self.drawingStrategy = drawingStrategy
        self.doubleDownExpected = None
        self.result = "Not initialize"
        self.noDrawCount = 0
        self.allDraw = 0
        #self.depthCounts = [0, 0, 0, 0, 0]
        self.depthCounts = []

    def printDrawStats(self):
        print(self.allDraw, self.depthCounts)

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

    def cardPlaying(self):
        if self.drawingStrategy == "naive":
            self.naivePlaying()
        elif self.drawingStrategy == "online":
            self.onlineStrategy()
        elif self.drawingStrategy == "calculate":
            self.calculateCardPlaying()
        else:
            raise Exception("No specified strategy in card playing")

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
        if self.splitStrategy=="none":
            return False
        elif self.splitStrategy=="online":
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
        elif self.splitStrategy=="calculate":
            if self.cards[0]==self.cards[1]:
                remainings = self.dealer.getRemaining()
                dealerFirstCard = self.dealer.getFirst()
                splitExpected = oneCardExpected(self.cards[0], self.hasAce, dealerFirstCard, remainings)
                origExpected = self.getExpectedValue()
                print("Splitting: ", origExpected, splitExpected, self.doubleDownExpected, dealerFirstCard, self.cards)
                if splitExpected*2 <= origExpected:
                    return False
                summ = sum(self.cards)
                if 9<=summ<=11:
                    self.doubleDownExpected = expectedDoubleDown(summ, self.hasAce, dealerFirstCard, remainings)
                    if self.doubleDownExpected>splitExpected:
                        return False
                print("Splitting: ", origExpected, splitExpected, self.doubleDownExpected, dealerFirstCard, self.cards)
                self.executeSplittingPairs()
                return True
            return False
        else:
            raise Exception("No specified double splitting pair")  

    def executeSplittingPairs(self):
        #Get base card and get a card for the first round
        baseCard = self.cards.pop()
        self.cards.append(self.dealer.givePlayerCard())
        # Execute first pair
        if not self.isBlackJack():
            self.cardPlaying()
        self.secondResult = self.result
        # Execute second pair
        self.cards = [baseCard]
        self.cards.append(self.dealer.givePlayerCard())
        if not self.isBlackJack():
            self.cardPlaying()

    def doubleDown(self):
        summ = sum(self.cards)
        if summ<9 or summ >11:
            return False
        if self.doubleStrategy=="none":
            return False
        elif self.doubleStrategy=="online":
            dealerFirstCard = self.dealer.getFirst()
            if summ==11:
                self.executeDoubleDown()
                return True
            if summ==10 and (dealerFirstCard!=10 or dealerFirstCard!=1):
                self.executeDoubleDown()
                return True
            if summ==9 and (2<=dealerFirstCard<=6):
                self.executeDoubleDown()
                return True
        elif self.doubleStrategy=="calculate":
            dealerFirstCard = self.dealer.getFirst()
            remainings = self.dealer.getRemaining()
            # Expected value of playing directly
            origExpected = self.getExpectedValue()
            if self.doubleDownExpected==None:
                self.doubleDownExpected = expectedDoubleDown(summ, self.hasAce, dealerFirstCard, remainings)
            # Check whether the expected value is positive
            if self.doubleDownExpected*2>=origExpected:
                self.executeDoubleDown()
                return True
        else:
            raise Exception("No specified double Down strategy")
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
        self.allDraw += 1
        while toDraw(points, self.hasAce, self.dealer.getFirst(), self.dealer.getRemaining(), 2, self.depthCounts):
            self.cards.append(self.dealer.givePlayerCard())
            if self.cards[-1]==1:
                self.hasAce = 1
            points += self.cards[-1]
            if points>21:
                break
            self.allDraw += 1
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
        self.doubleDownExpected = None
