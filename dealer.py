from collections import defaultdict
from deck import Deck
from utils import getDealerPointsDistribution

class Dealer:
    def __init__(self, deck):
        self.deck = deck
        self.reset()
        

    def printCards(self):
        print("Dealer cards:", self.cards, "result", self.finalVal)

    def isBlackJack(self):
        assert len(self.cards)==2, "Dummy blackJacke call, # of dealer's cards != 2"
        if self.cards[0]+self.cards[1]==11:
            if self.cards[0]==1 or self.cards[1]==1:
                self.finalVal = "BlackJack"
                return True
        return False

    # Return the remaining cards to the users(need to add the second card because user do not know value of the dealer's second card)
    def getRemaining(self):
        remainings = self.deck.getRemainings().copy()
        if len(self.cards)==1:
            return remainings
        remainings[self.cards[1]] += 1
        return remainings

    # Give card to player
    def givePlayerCard(self):
        return self.deck.drawCard()
    
    # Get the value of first card of the dealer
    def getFirst(self):
        assert len(self.cards)>0, "No first card"
        return self.cards[0]

    # Get card from deck to dealer's hands
    def recieveCard(self):
        self.cards.append(self.deck.drawCard())
        if self.cards[-1]==1:
            self.hasAce = 1
        self.value += self.cards[-1]

    # Get specific card from deck to dealer's hands
    def recieveSpecificCard(self, card):
        self.cards.append(card)
        if self.cards[-1]==1:
            self.hasAce = 1
        self.value += self.cards[-1]
    
    def reset(self):
        self.cards = []
        self.value = 0
        self.hasAce = 0
        self.finalVal = -1

    def takeCards(self):
        while self.value<17 and (self.value+10*self.hasAce<17 or self.value+10*self.hasAce>21):
            self.recieveCard()
        if self.value > 21:
            self.finalVal = -1
        else:
            if self.value+10*self.hasAce<=21:
                self.finalVal = self.value+10*self.hasAce
            else:
                self.finalVal = self.value
        return self.finalVal

def simulateDealer(size):
    deck = Deck()
    dealer = Dealer(deck)
    occurs = defaultdict(int)
    for _ in range(size):
        # Get first two cards
        dealer.recieveCard()
        dealer.recieveCard()
        # Take cards until >=17 or boom
        occurs[dealer.takeCards()] += 1
        dealer.reset()
        deck.reInit()
    deck.assertion()
    print([(key, float(value)/size) for key, value in occurs.items()])
    print(sum(occurs[key] for key in occurs))

if __name__=="__main__":
    # Simulation final points distribution for the dealer 
    #  simulateDealer(100000)

    # Simulation final points distribution for dealer with specific first card  
    # for i in range(1, 11):
    #     print(i)
    #     simulateWithFirstCards(i, 100000)
    simulateWithFirstCards(1, 1)
    pass


