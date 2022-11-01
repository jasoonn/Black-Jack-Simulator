from collections import defaultdict
from deck import Deck

# Calculate the probabilites to win the dealer at the given points
# return Type tuple (WinProb, loseProb, tieProb)
def gameProb(points, dealerFirstCard, remainings):
    if points==-1:
        return 0, 1, 0
    dealerDistribution = dealerDistributionWithFirst(dealerFirstCard, remainings)
    win = 0
    lose = 0
    tie = 0
    for key, value in dealerDistribution.items():
        if key==-1:
            win += value
        else:
            if key==points:
                tie += value
            elif key>points:
                lose += value
            else:
                win += value
    return (win, lose, tie)
    


# First calculate the probability to win the game if not
# Second 
def toDraw(points, hasAce, remainings):
    size = float(sum([v for v in remainings.values()]))
    answer = defaultdict(float)
    currentAce = hasAce
    for i in range(1, 11):
        if i==1:
            hasAce = 1
        occurProb = remainings[i]/size
        val = points + i
        if val>21:
            answer[-1] += occurProb
        else:
            if val+10*hasAce<=21:
                answer[val+10*hasAce] += occurProb
            else:
                answer[val] += occurProb
        if i==1:
            hasAce = currentAce

# Get the dealer final points distribution given that the dealer's first card is "first". Excluding the probability of black jack
def dealerDistributionWithFirst(first, remainings):
    # The dealer has 10 card, then the second card must not be Ace.
    baseSize = float(sum([count for count in remainings.values()]))
    if first==10:
        size = baseSize - remainings[1]
        answer = defaultdict(float)
        for i in range(7, 11):
            answer[10+i] += remainings[i]/size
        for i in range(2, 7):
            occurProb = remainings[i]/size
            remainings[i] -= 1
            for key, prob in getDealerPointsDistribution(10+i, 0, remainings, baseSize-1).items():
                answer[key] += prob*occurProb
            remainings[i] += 1
        return answer
    elif first==1:
        size = baseSize - remainings[10]
        answer = defaultdict(float)
        for i in range(6, 10):
            answer[11+i] += remainings[i]/size
        for i in range(1, 6):
            occurProb = remainings[i]/size
            remainings[i] -= 1
            for key, prob in getDealerPointsDistribution(1+i, 1, remainings, baseSize-1).items():
                answer[key] += prob*occurProb
            remainings[i] += 1
        return answer
    else:
        return getDealerPointsDistribution(first, 0, remainings, baseSize)

    

    
# Get the dealer distribution given that the dealer has "points" points
def getDealerPointsDistribution(points, hasAce, remainings, remainSize):
    answer = defaultdict(float)
    currentAce = hasAce
    # Handle the rest cards
    for i in range(1, 11):
        if i==1:
            hasAce = 1
        occurProb = remainings[i]/remainSize
        val = points + i
        if val >21:
            answer[-1] += occurProb
            continue
        if val<17 and (val+10*hasAce<17 or val+10*hasAce>21):
            remainings[i] -= 1
            for key, prob in getDealerPointsDistribution(val, hasAce, remainings, remainSize-1).items():
                answer[key] += prob*occurProb
            remainings[i] += 1
        else:
            if val>21:
                answer[-1] += occurProb
            else:
                if val+10*hasAce<=21:
                    answer[val+10*hasAce] += occurProb
                else:
                    answer[val] += occurProb
        if i==1:
            hasAce = currentAce
    return answer

if __name__=="__main__":
    # Test for getDealerPointsDistribution
    # deck = Deck()
    # answer = getDealerPointsDistribution(0, 0, deck.getRemainings(), 52*6.0)
    # print("Return", answer, sum([i for i in answer.values()]))

    # Test for  dealerDistributionWithFirst
    for i in range(1, 11):
        deck = Deck()
        cardDraw = i
        deck.drawSpecificCard(cardDraw)
        answer = dealerDistributionWithFirst(cardDraw, deck.getRemainings())
        print(cardDraw, "Return", answer, sum([i for i in answer.values()]))
    # print(gameProb(17, cardDraw, deck.getRemainings()))
