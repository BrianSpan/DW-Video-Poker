from dwconstants import *
from dwnamehands import *
from collections import Counter
from dwpartial import *

############
# Determine which cards to hold based on strategy of how many wild cards
############

def makehold(handinfo)->list[bool]:
    out=[True]*5
    handinfo.discards=[]
    
    #4 wildcards
    if handinfo.wilds==4: #Keep 4 Deuces
        pass  #discards have already been calculated
    
    #3 wildcards
    elif handinfo.wilds==3:
        if handinfo.handscore==WILDROYALFLUSH:
            pass  #discards have already been calculated
        elif handinfo.handscore==FIVEKIND:
            pass  #discards have already been calculated
        else: #junk all but wild
            handinfo.discards=[cardpos
                               for cardpos in range(5)
                               if (rank:=handinfo.hand[cardpos][0])!=WILD]
    
    #2 wildcards
    elif handinfo.wilds==2:
        if handinfo.handscore==WILDROYALFLUSH:
            pass  #discards have already been calculated
        elif handinfo.handscore==FIVEKIND:
            pass  #discards have already been calculated
        elif handinfo.handscore==STRAIGHTFLUSH:
            pass  #discards have already been calculated
        elif handinfo.handscore==FOURKIND:
            #determine the card that isnt matching
            badcard=[handinfo.hand.index((rank,suit))
                     for rank,suit in handinfo.hand
                     if handinfo.nowildranks.count(rank)==1]
            handinfo.discards=badcard
        elif partial_w2_4ofwildroyalflush(handinfo):
            pass  #discards have already been calculated
        elif partial_w2_4ofstraightflushexcept(handinfo):
        #w2suitconx(handinfo):
            pass  #discards have already been calculated
        else: #junk
            handinfo.discards=[cardpos
                               for cardpos in range(5)
                               if (rank:=handinfo.hand[cardpos][0])!=WILD]
            #handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if rank!=WILD]
    
    #1 wildcard
    elif handinfo.wilds==1:
        if handinfo.handscore==WILDROYALFLUSH:
            pass  #discards have already been calculated
        elif handinfo.handscore==FIVEKIND:
            pass  #discards have already been calculated
        elif handinfo.handscore==STRAIGHTFLUSH:
            pass  #discards have already been calculated
        elif handinfo.handscore==FOURKIND:
            badcard=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if handinfo.nowildranks.count(rank)==1][0]
            handinfo.discards=[badcard]
        elif partial_w1_4ofroyalflush(handinfo):
            pass  #discards have already been calculated
        elif is_wild_fullhouse(handinfo): #fullhouse   #wizardofodds.com
            pass  #discards have already been calculated
        elif is_wild_flush(handinfo): #flush www.888casino.com
            pass  #discards have already been calculated
        elif partial_w1_4ofoutsidestraightflush(handinfo): #4 to Straight Flush, 3 consecutive cards, 567 and higher #casino.guru
            pass  #discards have already been calculated 
        elif is_straight(handinfo): #ST   888casino.com
            #straight function already includes wild or not
            pass  #discards have already been calculated
        elif is_wild_threekind(handinfo):
            pass  #discards have already been calculated
        elif  partial_w1_4ofinsidestraightflush(handinfo):# 4 ISF, 4 low or higher. www.888casino.com
            pass  #discards have already been calculated
        elif partial_w1_3ofroyalflush(handinfo): #3 to Royal Flush
            pass  #discards have already been calculated
        elif partial_w1_3ofstraightflush(handinfo):  #3 to Straight Flush, 2 consecutive cards, 67 and higher
            pass  #discards have already been calculated    
        else: #junk
            handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if rank!=WILD]
    
    # No wildcards
    elif handinfo.wilds==0:
        if handinfo.handscore==NATROYALFLUSH:
            handinfo.discards=[]
        elif partial_w0_4ofroyalflush(handinfo):
            pass  #discards have already been calculated
        elif handinfo.handscore==STRAIGHTFLUSH:
            handinfo.discards=[]
        elif handinfo.handscore==FOURKIND:
            #badcard=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if handinfo.nowildranks.count(rank)==1][0]
            badcard=[pos for pos,(rank,suit) in enumerate(handinfo.hand) if handinfo.nowildranks.count(rank)==1]
            handinfo.discards=[badcard]
        elif handinfo.handscore==FULLHOUSE:
            handinfo.discards=[]
        elif handinfo.handscore==FLUSH:
            handinfo.discards=[]
        elif handinfo.handscore==STRAIGHT:
            handinfo.discards=[]
        elif is_w0_threekind(handinfo):
            pass  #discards have already been calculated
        elif partial_w0_4ofstraightflush(handinfo): #4 to Straigth Flush  - doesnt specify isf or osf
            out=[not(i in handinfo.discards) for i in range(5)]
        elif partial_w0_3ofroyalflush(handinfo):#3 to a royal flush
            pass  #discards have already been calculated
        elif partial_w0_4offlush(handinfo):#4 FL
            pass  #discards have already been calculated
        elif handinfo.handscore==TWOPAIR or handinfo.handscore==PAIRJACK or handinfo.handscore==PAIR:
            pass  #discards have already been calculated
        elif partial_w0_4ofoutsidestraight(handinfo):#4 to an outside straight
            pass  #discards have already been calculated
        elif partial_w0_3ofstraightflush(handinfo): #3 to straight flush
            pass  #discards have already been calculated
        elif partial_w0_4ofinsidestraight(handinfo):#4 to an inside straight, except missing deuce
            pass  #discards have already been calculated
        else:#junk
            handinfo.discards=list(range(5)) #all 5
        
    out=[not(cardindex in handinfo.discards) for cardindex in range(5)]    
    return(out)

###########
#
# Helper function
#
##########
def creatediscard( hand:list[tuple[str,str]], cond:callable)->list[int]:
    """
    Return list of dicard in order (0-based)
    based on not fitting pattern
    
    Args:
    hand:The original hand to choose from
    condition: lambda function
        Args: rank: rank of card
              suit:suit of card
        Output: True if discard      
    Output:
    list of positions (0-based) that can be discarded
    """
    #ex: creatediscards(handinfo.hand, lambda rank,suit: rank!=WILD and rank not in ROYAL)
    #ex: hand.discards=creatediscards(handinfo.hand, lambda rank,suit: rank!=WILD and suit==badsuit)
    out=[pos for pos,(rank,suit) in enumerate(hand) if cond(rank,suit)]
    
    return(out)    

