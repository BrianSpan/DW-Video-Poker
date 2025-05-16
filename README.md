#Part of a portfolio of Python projects developed by Brian Spangler

###Deuces Wild Video Poker simulation
Demonstration on classes, list methods and comprehensions

###Introduction
Most casino games have a Return To Player (RTP) of less that 100%, meaning the odds are in the favor of the casino.
However this are a few games where, when played correctly, have an RTP of over 100% meaning that the odds are in the favor of the player.
One of these game is Full Pay Deuces Wild Video Poker. The RTP is 100.76% when played correctly.
Deuces Wild means, of course, that 2's are considered wildcards. "Full Pay" means the paytable for many hands is generous compared to other variations.
The caveat to this payoff is that the game must be played with optimal strategy.

###Quick introduction to Video Poker
After placing a bet, the player triggers the machine to deal a 5 card draw poker hand. The player can choose to keep any or all cards in an attempt to get he best poker hand.
After replacing the discarded cards, the machine pays off according to it's payoff rate.

### Full Pay Deuces Wild pay table
|Hand|Payoff
|---|---
|Natural Royal Flush|800
|Four Deuces|200
|Wild Royal Flush|25
|Five of a Kind|15
|Straight Flush|9
|Four of a kind|5
|Full House|3
|Flush|2
|Straight|2
|Three of a kind|1
|Nothing|0

###What this simulation does
For each round, bet is automatically placed, then a hand of 5 cards is displayed. If it makes a recognized named hand, this is displayed.
Then the best strategy to hold cards is created, the discarded cards are replaced and the hand is named again and any payout made. This continues until exit conditions are done.

This program also simulates a betting strategy. A very common strategy for betting is going in with a set amount and playing until it's gone.
This is just a way to spend money and not test strategy.The stratagy I use here is to put the money in several smaller pots. In this case, I made the total pot 1000 and 10 smaller pots of 100. Each wager would be $5 representing a full 5 coin bet.
You gamble just the money in that smaller pot until you hit one of the stop conditions, one of which is dipping below a certain percentage. This minimizes loss.
For this simulation, I made the stop conditions: having 70% or less of the smaller pot, having more than 100 rounds in one small pot (to prevent infinite games of winning and losing)),
and the first time the player makes Straight Flush in this round. This last condition avoids risking an amount won even if it does end up making a limit to how much can be won.

###How it works
For the first deal, I call deal() from dwdeal.py to make 10 cards. The initial 5 and an additional 5 to draw from.
I call the DWpoker class in dwclass.py which collects several facts about the hand including number of wild cards,the ranks, the suits, versions of hands without wildcards, etc.
I also call namehand() in dwnamehands.py. This calls other functions named after hands to do pattern matching to name the hand.
I then call makehold() in dwmakehold.py to determine the best cards to hold based on strategy outlined below. This relies on many partial hand pattern reconition functions in the same file.
After swapping discarded cards (using swaphands() in dwmakedeal.py), I apply namehand() again and pay off any odds. I check if any stop conditions are met in the smaller pot and keep repeating until I reach stop conditions for all smaller pots.


###Strategy used to determine discards
You would easily be forgiven to think that the best computer way of determining the best way to figure the cards to discard would be to cycle through every possible replacement card. This gets to an absurd amount quickly.
To cycle through only replacing only one card in the hand would be 47 cards times all 5 positions or 235. Replacing 2 cards in a hand is over 22 thousand. The numbers get much higher as we go through combinations to replece more and more cards.
Computers still just arent fast enough to go through that many combinations.

Instead, I did it the "human way". Several websites have already created strategies to try to have a player recognize the best potential hand. They break all the strategies dow based on how many wild cards are in the hand.
Some sources I used for strategies are:
- https://www.888casino.com/blog/video-poker-deuces-wild-strategy
- https://wizardofodds.com/games/video-poker/strategy/deuces-wild/full-pay/simple/
- https://casino.guru/deuces-wild
- https://digitalscholarship.unlv.edu/cgi/viewcontent.cgi?article=1229&context=grrj

###Features:
Cards are displayed with the appropriate suit symbol
Can set TESTMODE to True in dwconstants.py to use a test file instead of random
Optional output of data with DEBUG

###How to Run
```
python dwvpeval
```

###Files included and purpose
dwclass.py  - Holds the class DWpokerinfo
dwconstants.py - Constants such as hand names used for self-documenting and payout tables
dwdeal.py - deal(), swaphands() and auxilkiary functions
dwmakehold.py - creates a list of which cards to hold. Has functions to recognize partial hands
dwnamehands.py - namehand() and other functions to recognize patterns of completed handshands
dwvpeval.py - the main program that works as a framework for the output
pokertest.txt - a sample of hands to be used as a control
README.me - this file


###Dependencies:
Python 3.7+
import random to use the sample function

###Sample output:
```
Starting Pot for this round: 100
Round: 1 Turn: 1 Wagering: $5 New total: $95
2♠ T♥ 6♦ K♦ J♣
Nothing (Pair) - Payout:0
HOLD DROP DROP DROP DROP
2♠ 7♥ Q♠ 5♣ 2♦ Three of a kind Payout:5
Total Pot: 100

Round: 1 Turn: 2 Wagering: $5 New total: $95
4♣ Q♣ 9♦ J♠ 7♣
Nothing - Payout:0
DROP DROP DROP DROP DROP
Q♠ 7♥ 6♣ 6♠ 9♣ Nothing (Pair) Payout:0
Total Pot: 95

Round: 1 Turn: 3 Wagering: $5 New total: $90
T♦ T♥ 9♠ Q♦ T♠
Three of a kind - Payout:5
HOLD HOLD DROP DROP HOLD
T♦ T♥ J♥ 7♦ T♠ Three of a kind Payout:5
Total Pot: 95

Round: 1 Turn: 4 Wagering: $5 New total: $90
Q♠ 7♦ 4♦ 6♣ 8♦
Nothing - Payout:0
DROP HOLD HOLD DROP HOLD
T♥ 7♦ 4♦ 8♠ 8♦ Nothing (Pair) Payout:0
Total Pot: 90

Round: 1 Turn: 5 Wagering: $5 New total: $85
2♥ A♠ T♠ 7♥ K♥
Nothing (Pair) - Payout:0
HOLD DROP DROP DROP DROP
2♥ Q♥ 2♣ T♥ 6♥ Flush Payout:20
Total Pot: 105

.
.
.

Pot:  1 
Number of rolls:  7 
Amount: $ 70 

Pot:  2 
Number of rolls:  3 
Amount: $ 190 

Pot:  3 
Number of rolls:  15 
Amount: $ 70 

.
.
.

Total rolls:  92
Total take: $ 1040
```

###Future enhancements:
Change hard-coded odds to simulate non Full Pay
Create options for various other video poker games that have RTP over 100%
Choose testfile if TESTMODE=True instead of hardcoded pokertest.txt