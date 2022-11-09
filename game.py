from collections import defaultdict
from dealer import Dealer
from player import Player
from deck import Deck

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
        while round<numRound:
            if round%100==0:
                print("round", round)
            if round%1000==0:
                print(round, counts)
            thisRoundBet = []
            result = []
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
                for player in self.players:
                    if player.isBlackJack():
                        continue
                    # Check whether they want doubling down

                    # Check whether they want to split pairs
                    
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
                    elif result[-1]=='T':
                        earned[idx] += thisRoundBet[idx]
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
            assert sum(count.values())==numRound
            print("Spent:", spent[idx], " Earn: ", earned[idx])



if __name__=="__main__":
    game = Game(1)
    game.startGame(1000000)