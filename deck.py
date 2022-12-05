from collections import defaultdict
import random

class Deck:
    def __init__ (self):
        self.reInit()
    
    # Let the cards become six packs
    def reInit(self):
        #Six packs
        self.cards = []
        for i in range(1, 10):
            for _ in range(4*6):
                self.cards.append(i)
        for _ in range(4*4*6):
            self.cards.append(10)
        self.remainingCards = {}
        for i in range(1, 10):
            self.remainingCards[i] = 4*6
        self.remainingCards[10] = 4*4*6

    # Return a random card from the remaining
    def drawCard(self):
        if len(self.cards)==0:
            print("No card to draw. Please call the reInit() function")
            return 0
        idx = random.randint(0, len(self.cards)-1)
        self.remainingCards[self.cards[idx]] -= 1
        return self.cards.pop(idx)

    # Draw a specific card
    def drawSpecificCard(self, card):
        assert self.remainingCards[card]>0, "Not enough "+card
        self.remainingCards[card] -= 1
        idx = 0
        while idx<len(self.cards):
            if self.cards[idx]==card:
                self.cards.pop(idx)
                break
            idx += 1  

    def getRemainings(self):
        return self.remainingCards

if __name__=="__main__":
    deck = Deck()
    counts = defaultdict(int)
    for _ in range(312):
        counts[deck.drawCard()] += 1
    print(counts)
    counts = defaultdict(int)
    deck.reInit()
    for _ in range(10):
        counts[deck.drawCard()] += 1
    print(counts)

    