Black Jack Simulator
===
### Goal
Provide simulation result of black jack under different strategies.
### Quick Start
```
# Run simulation with naive strategy without considering splitting and double down
python main.py --split none --double none --draw naive
# Run simulation with online strategies for drawing, splitting pair, and double down
python main.py --split online --double online --draw online
# Run simulatoin with calculate strategies for drawing, splitting pair, and double down
python main.py --split calculate --double calculate --draw calculate
```
Online strategy [reference](https://bicyclecards.com/how-to-play/blackjack/).
### Split Pair  Strategy
* Online: Split a pair of aces or 8s; identical ten-cards should not be split, and neither should a pair of 5s, since two 5s are a total of 10, which can be used more effectively in doubling down. A pair of 4s should not be split either, as a total of 8 is a good number to draw to. Generally, 2s, 3s, or 7s can be split unless the dealer has an 8, 9, ten-card, or ace. Finally, 6s should not be split unless the dealer's card is poor (2 through 6).
* Calculate: Calculate the expected value of playing normaly, the expected value of splitting pair, and the expected value of double down(when 9<=points<=11). If the expected value of splitting pair is the largest. Then, we choose to split the pair.

### Double Down Strategy
* Online:Double down with a total of 11. With a total of 10, double down unless the dealer shows a ten-card or an ace. With a total of 9, double down only if the dealer's card is fair or poor (2 through 6).
* Calculate: Calculate the expected value of playing normaly and the expected value of double down. If the expected value of splitting pair is the largest. Then, we choose to double down.

### Drawing Strategy
* Naive: Continue to take cards until the total is 17.
* Online: When the dealer's upcard is a good one, a 7, 8, 9, 10-card, or ace, keep drawing until a total of 17 or more is reached. When the dealer's upcard is a poor one, 4, 5, or 6, stop drawing as soon as a total of 12 or higher. Finally, when the dealer's up card is a fair one, 2 or 3, the player should stop with a total of 13 or higher.
* Calculate: Our algorithm will first calculate the expected gain of not drawing the card. Then, it calculates the expected gain of drawing one card under consideration of a given depth. If the non-drawing expected gain is greater than the drawing expected one, we will decide not to draw the card. If the drawing expected gain is greater than the non-drawing expected one, we will decide to draw the card. 

### How depth the algorithm should go
If the depth is large, it takes more time to calculate value. 
If the depth is small, the accuracy of the expected value is decreased, which might harm the algorithm.
To strike a balance between these two, we simulate .
100000, [53951, 797, 825, 827, 827]
If we go with depth=0, we will miss about 797
