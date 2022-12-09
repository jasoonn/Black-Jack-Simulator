from cgitb import reset
from collections import defaultdict
from dealer import Dealer
from player import Player
from deck import Deck

class Game:
    def __init__(self, numPlayers, splitStrategy, doubleStrategy, drawingStrategy):
        self.deck = Deck()
        self.dealer = Dealer(self.deck)
        self.players = [Player(i, self.dealer, splitStrategy, doubleStrategy, drawingStrategy) for i in range(numPlayers)]
        
    def startGame(self, numRound, shuffleEach=False):
        round = 0
        spent = [0 for _ in self.players]
        earned = [0 for _ in self.players]
        counts = [defaultdict(int) for _ in self.players]
        splittingEarn = [0 for _ in self.players]
        splittingSpend = [0 for _ in self.players]
        doubleEarn = [0 for _ in self.players]
        doubleSpent = [0 for _ in self.players]
        while round<numRound:
            if round%1000==0:
                print(round, counts)
            thisRoundBet = []
            result = []
            isSplitting = [False for _ in self.players]
            #Give first card
            for player in self.players:
                thisRoundBet.append(1)
                player.recievedCard(self.dealer.givePlayerCard())
            self.dealer.recieveCard()
            #Give second card
            for player in self.players:
                player.recievedCard(self.dealer.givePlayerCard())

            self.dealer.recieveCard()
            
            #Check whether the dealer is blackjack
            if self.dealer.isBlackJack():
                for idx, player in enumerate(self.players):
                    if player.isBlackJack():
                        counts[idx]["T"] += 1
                        result.append("T")
                        earned[idx] += thisRoundBet[idx]
                    else:
                        counts[idx]["L"] += 1
                        result.append("L")
            else:
                #Serve every players and the dealer
                for idx, player in enumerate(self.players):
                    if player.isBlackJack():
                        continue
                    # Check whether they want to split pairs
                    if player.splittingPairs():
                        isSplitting[idx] = True
                    # Check whether they want doubling down
                    elif player.doubleDown():
                        thisRoundBet[idx] *= 2
                        doubleSpent[idx] += thisRoundBet[idx]
                    else:
                        player.cardPlaying()
                dealerPoint = self.dealer.takeCards()
                #Check the result
                for idx, player in enumerate(self.players):
                    counts[idx][player.checkWin(dealerPoint)] += 1
                    result.append(player.checkWin(dealerPoint))
                    if result[-1]=='B':
                        earned[idx] += thisRoundBet[idx]*2.5
                    elif result[-1]=='W':
                        earned[idx] += thisRoundBet[idx]*2
                        if thisRoundBet[idx]>1:
                            doubleEarn[idx] += thisRoundBet[idx]*2
                        if isSplitting[idx]:
                            splittingEarn[idx] += thisRoundBet[idx]*2
                    elif result[-1]=='T':
                        earned[idx] += thisRoundBet[idx]
                        if thisRoundBet[idx]>1:
                            doubleEarn[idx] += thisRoundBet[idx]
                        if isSplitting[idx]:
                            splittingEarn[idx] += thisRoundBet[idx]
                    # Do another round for splitting pair
                    if isSplitting[idx]:
                        result[-1] = [result[-1]]
                        counts[idx][player.checkSecondWin(dealerPoint)] += 1
                        result[-1].append(player.checkSecondWin(dealerPoint))
                        if result[-1][-1]=='B':
                            earned[idx] += thisRoundBet[idx]*2.5
                            splittingEarn[idx] += thisRoundBet[idx]*2.5
                        elif result[-1][-1]=='W':
                            earned[idx] += thisRoundBet[idx]*2
                            splittingEarn[idx] += thisRoundBet[idx]*2
                        elif result[-1][-1]=='T':
                            earned[idx] += thisRoundBet[idx]
                            splittingEarn[idx] += thisRoundBet[idx]
                        thisRoundBet[idx] *= 2
                        splittingSpend[idx] += thisRoundBet[idx]

            for idx in range(len(self.players)):
                spent[idx] += thisRoundBet[idx]
                    
            #print(result)
            #self.dealer.printCards()
            for player in self.players:
                #player.printCards()
                player.reset()
            self.dealer.reset()
            if shuffleEach or sum(self.deck.getRemainings().values())<70:
                self.deck.reInit()
            round += 1
        # Output simulation statistics
        for idx, count in enumerate(counts):
            assert sum(count.values())==numRound+splittingSpend[idx]/2
            print("Overall result:", count)
            print("Spent:", spent[idx], " Earn: ", earned[idx], " Adjust earn ", earned[idx]/spent[idx]*numRound)
            print("Double spent:", doubleSpent[idx], "Double earned", doubleEarn[idx])
            print("Splitting spent:", splittingSpend[idx], "Splitting earned", splittingEarn[idx])

if __name__=="__main__":
    game = Game(1, "none", "none", "calculate")
    game.startGame(100000)
    #game.startGame(10000, True)
    #checkExpected(50000)