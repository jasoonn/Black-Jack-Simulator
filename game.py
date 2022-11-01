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
        while round<numRound:
            result = []
            #Give first card
            for player in self.players:
                player.recievedCard(self.dealer.givePlayerCard())
            self.dealer.recieveCard()
            #Give second card
            for player in self.players:
                player.recievedCard(self.dealer.givePlayerCard())
            self.dealer.recieveCard()
            #Check whether the dealer is blackjack
            if self.dealer.isBlackJack():
                for player in self.players:
                    if player.isBlackJack():
                        result.append("T")
                    else:
                        result.append("L")
            else:
                #Serve every players and the dealer
                for player in self.players:
                    player.naivePlaying()
                dealerPoint = self.dealer.takeCards()
                #Check the result
                for player in self.players:
                    result.append(player.checkWin(dealerPoint))
            print(result)
            self.dealer.printCards()
            for player in self.players:
                player.printCards()
                player.reset()
            self.dealer.reset()
            round += 1


if __name__=="__main__":
    game = Game(5)
    game.startGame(3)