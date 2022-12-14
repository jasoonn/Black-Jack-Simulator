from collections import defaultdict
from deck import Deck

# Calculate the probabilites to win the dealer at the given points
# return Type tuple (WinProb, loseProb, tieProb)
def gameProb(points, hasAce, dealerFirstCard, remainings):
    if points==-1:
        return -1
    if points+10*hasAce<=21:
        points = points+10*hasAce
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
    return win-lose

# Get the expected value when the player has only one card(used in splitting pair)
def oneCardExpected(card, hasAce, dealerFirstCard, remainings):
    size = float(sum([v for v in remainings.values()]))
    currentAce = hasAce
    expectedValue = 0
    for i in range(1, 11):
        if remainings[i]==0:
            continue
        occurProb = remainings[i]/size
        if (i==1 and card==10) or (i==10 and card==1):
            expectedValue += occurProb*1.5
            continue
        if i==1:
            hasAce = 1
        remainings[i]-=1
        val = card + i
        if val>21:
            expectedValue -= occurProb
        else:
            expectedValue += occurProb*gameProb(val, hasAce, dealerFirstCard, remainings)
        if i==1:
            hasAce = currentAce
        remainings[i]+=1
    return expectedValue

def expectedDoubleDown(points, hasAce, dealerFirstCard, remainings):
    size = float(sum([v for v in remainings.values()]))
    currentAce = hasAce
    expectedValue = 0
    for i in range(1, 11):
        if remainings[i]==0:
            continue
        occurProb = remainings[i]/size
        remainings[i] -= 1
        if i==1:
            hasAce = 1
        expectedValue += occurProb*gameProb(points+i, hasAce, dealerFirstCard, remainings)
        remainings[i] += 1
        if i==1:
            hasAce = currentAce
    return expectedValue

# Find the expected value with at least two cards 
def expectedWin(points, hasAce, dealerFirstCard, remainings):
    if toDraw(points, hasAce, dealerFirstCard, remainings, 1)==False:
        return gameProb(points, hasAce, dealerFirstCard, remainings)
    else:
        size = float(sum([v for v in remainings.values()]))
        currentAce = hasAce
        expectedValue = 0
        for i in range(1, 11):
            if remainings[i]==0:
                continue
            if i==1:
                hasAce = 1
            occurProb = remainings[i]/size
            remainings[i]-=1
            val = points + i
            if val>21:
                expectedValue -= occurProb
            else:
                expectedValue += occurProb*expectedWin(val, hasAce, dealerFirstCard, remainings)
            if i==1:
                hasAce = currentAce
            remainings[i]+=1
        return expectedValue

def calculateExpectedWithDepth(points, hasAce, dealerFirstCard, remainings, depth=1):
    size = float(sum([v for v in remainings.values()]))
    drawExpectedValue = 0
    currentAce = hasAce
    for i in range(1, 11):
        if remainings[i]==0:
            continue
        if i==1:
            hasAce = 1
        occurProb = remainings[i]/size
        val = points + i
        remainings[i]-=1
        if val>21:
            drawExpectedValue -= occurProb
        else:
            expected = gameProb(val, hasAce, dealerFirstCard, remainings)
            if depth>1:
                expected = max(expected, calculateExpectedWithDepth(val, hasAce, dealerFirstCard, remainings, depth-1))
            drawExpectedValue += occurProb*(expected)
        remainings[i]+=1
        if i==1:
            hasAce = currentAce
        
    return drawExpectedValue

# First calculate the probability to win the game if not
# Second iterate through all the possibilities
def toDraw(points, hasAce, dealerFirstCard, remainings, depth=1, logging=[]):
    noDrawExpectedValue = gameProb(points, hasAce, dealerFirstCard, remainings)
    drawExpectedValue = calculateExpectedWithDepth(points, hasAce, dealerFirstCard, remainings, depth)
    if drawExpectedValue >= noDrawExpectedValue:
        return True
    else:
        for idx in range(1, len(logging)):
            if calculateExpectedWithDepth(points, hasAce, dealerFirstCard, remainings, depth=depth+idx)>noDrawExpectedValue:
                for i in range(idx, len(logging)):
                    logging[i] += 1
                break
        if len(logging)>0:
            logging[0] += 1
        return False


# Get the dealer final points distribution given that the dealer's first card is "first". Excluding the probability of black jack
#  Verified
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
# The function has been verified
def getDealerPointsDistribution(points, hasAce, remainings, remainSize):
    answer = defaultdict(float)
    currentAce = hasAce
    # Handle the rest cards
    for i in range(1, 11):
        if remainings[i]==0:
            continue
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
