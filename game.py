from cgitb import reset
from collections import defaultdict
from dealer import Dealer
from player import Player
from deck import Deck
import copy

class Game:
    def __init__(self, numPlayers):
        self.deck = Deck()
        self.dealer = Dealer(self.deck)
        self.players = [Player(i, self.dealer) for i in range(numPlayers)]
        
    def startGame(self, numRound):
        round = 0
        spent = [0 for _ in self.players]
        earned = [0 for _ in self.players]
        counts = [defaultdict(int) for _ in self.players]
        splittingEarn = [0 for _ in self.players]
        splittingSpend = [0 for _ in self.players]
        doubleEarn = [0 for _ in self.players]
        doubleSpent = [0 for _ in self.players]
        while round<numRound:
            if round%100==0:
                print("round", round)
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
                    # Check whether they want doubling down
                    # Check whether they want to split pairs
                    if player.splittingPairs():
                        isSplitting[idx] = True
                    elif player.memoryDoubleDown():
                    #elif player.doubleDown():
                        thisRoundBet[idx] *= 2
                        doubleSpent[idx] += thisRoundBet[idx]
                    else:
                        #player.naivePlaying(11)
                        #player.calculateCardPlaying()
                        player.onlineStrategy()
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
            if sum(self.deck.getRemainings().values())<70:
                print("reshuffle")
                self.deck.reInit()
            round += 1
        print(counts)
        #Verify
        for idx, count in enumerate(counts):
            assert sum(count.values())==numRound+splittingSpend[idx]/2
            print("Spent:", spent[idx], " Earn: ", earned[idx], " Adjust earn ", earned[idx]/spent[idx]*numRound)
            print("Double spent:", doubleSpent[idx], "Double earned", doubleEarn[idx])
            print("Splitting spent:", splittingSpend[idx], "Splitting earned", splittingEarn[idx])


def fixSimulation(simulationTimes):
    deck = Deck()
    dealer = Dealer(deck)
    player = Player(0, dealer)
    dealer.recieveCard()
    player.recievedCard(player.getDealer().givePlayerCard())
    player.recievedCard(player.getDealer().givePlayerCard())
    dealer.printCards()
    player.printCards()
    orig = copy.deepcopy(player)
    print("Expected value", player.getExpectedValue())
    total = 0
    iteration = 10
    outer = 0
    while outer<iteration:
        outer += 1
        win = 0
        tie = 0
        loss = 0
        count = 0
        while count<simulationTimes:
            # if count%10000==0:
            #     print(count)
            player.getDealer().recieveCard()
            #Skip if meet dealer black jack
            if player.getDealer().isBlackJack():
                player = copy.deepcopy(orig)
                continue
            count += 1
            player.calculateCardPlaying()
            result = player.checkWin(player.getDealer().takeCards())
            #player.getDealer().printCards()
            #player.printCards()
            #print(result)
            if result=='W':
                win += 1
            elif result=='T':
                tie += 1
            else:
                loss += 1

            player = copy.deepcopy(orig)
        print(win, loss , tie)
        total += (win-loss)
        print("Simulate expected:", (win-loss)/float(simulationTimes))
    print("ALL: ", total/float(simulationTimes*iteration))
    
    

if __name__=="__main__":
    # game = Game(1)
    # game.startGame(10000)
    fixSimulation(50000)