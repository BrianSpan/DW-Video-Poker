TESTMODE=True #T=read hands from a file,F=generate randomly
DEBUG=True #Display variables at different times

#global switches
if TESTMODE:
    readfilename='pokertest.txt'#pokertest.txt or p054_poker.txt
    d=open(readfilename, "r")
if DEBUG:
    writefilename="testingout.txt"
    q=open(writefilename, "a")

#hand names for self documenting
JUNK=0
PAIR=1
PAIRJACK=2
TWOPAIR=3
THREEKIND=4
STRAIGHT=5
FLUSH=6
FULLHOUSE=7
FOURKIND=8
STRAIGHTFLUSH=9
FIVEKIND=10
WILDROYALFLUSH=11
FOURWILD=12
NATROYALFLUSH=13

# text to display
NAMES = {
  JUNK: "Nothing", PAIR: "Nothing (Pair)", PAIRJACK: "Nothing (Jacks or better)",
  TWOPAIR: "Nothing (Two Pairs)", THREEKIND: "Three of a kind",
  STRAIGHT: "Straight", FLUSH: "Flush", FOURKIND: "Four of a kind",
  FULLHOUSE: "Full House", STRAIGHTFLUSH: "Straight Flush",
  FIVEKIND: "Five of a Kind", WILDROYALFLUSH: "Wild Royal Flush",
  FOURWILD: "Four Wild Cards",NATROYALFLUSH: "Natural Royal Flush"  
}

# Normal way to play is 5 coins.
# Each of these payouts are 1/5 of 5 coins
PAYOUT = { JUNK: 0, PAIR: 0, PAIRJACK: 0, TWOPAIR: 0,
  THREEKIND: 1, STRAIGHT: 2, FLUSH: 4, FULLHOUSE: 4,
  FOURKIND: 4, STRAIGHTFLUSH: 10, FIVEKIND:12,
  WILDROYALFLUSH:20,FOURWILD:200, NATROYALFLUSH: 800  
}

#constants
WILD='2'
SUITLIST=['D','C','H','S']
RANKLIST=['A','2','3','4','5','6','7','8','9','T','J','Q','K']
ROYAL=['J','Q','K','A','T']
HIGHCARDS=['J','Q','K','A']

#bank variables for betting strategy
BANK=1000
POT=100
BET=5
LOSSLIMIT=0.70
MAXTURNS=100
results=[(0,0)]*int(BANK/POT)

#card icons for display
ansired='\x1b[31m'
ansiblack='\x1b[30m'
ansireset='\x1b[0m'
diamondicon=ansired+'\u2666'+ansireset #red D
clubicon=ansiblack+'\u2663'+ansireset #black C
hearticon=ansired+'\u2665'+ansireset #red H
spadeicon=ansiblack+'\u2660'+ansireset #black S
iconlist=[diamondicon,clubicon,hearticon,spadeicon]
