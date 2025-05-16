from dwconstants import *
from random import sample


def deal()->tuple[list[int],list[tuple[str,str]]]:
    #make a set of 10 cards. The 1st 5 will be the hand,...
    #... the others will be shadow hand to draw from
    if TESTMODE:
        #I'm not using 'rank' and 'suit'. They are just there for readability
        inlist=(d.readline()).strip().upper().split(' ')[0:10]
        numberlist=[(RANKLIST.index(rank:=card[0]))
                   +(SUITLIST.index(suit:=card[1])*13)
                   for card in inlist]
        playerhand=[(rank:=card[0],suit:=card[1]) for card in inlist][0:5]
    else:
        numberlist=makenumbers()
        playerhand=makecards(numberlist)[0:5]
    return(numberlist,playerhand)


def swaphand(cardlist:list[int],hold:list[bool]) -> list[int]: #list of cards,list of 5 t/f
    newcards=cardlist.copy()
    for cardnum in range(5):
        if not(hold[cardnum]):
            newcards[cardnum]=newcards[5] #first "extra" card
            del newcards[5]
    return(newcards)


def makecards(cardnumlist:list[int])->list[tuple[str,str]]:
    out=[(RANKLIST[i%13],SUITLIST[int(i/13)])
          for i in cardnumlist]
    return out


def makenumbers(total:int=10)->list[int]:
    return sample(range(52),total)


def display_card(hand:list[tuple[str,str]])->list[tuple[str,str]]:
    out=[(rank,iconlist[SUITLIST.index(suit)]) for rank,suit in hand]
    return (out)
