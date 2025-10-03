from dwconstants import *
from dwnamehands import *
from collections import Counter

##########
# Partial hand functions
#
# Recognize a pattern in partial hands
#
##########
#
# wilds=0
#
##########
def partial_w0_4ofroyalflush(handinfo: "DWpokerinfo") -> bool:
    """
    Check if a hand with 0 wilds contains exactly 4 cards to a Royal Flush.
    Record discards in handinfo.
    Assumes: 0 wild cards
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False

    #make a royal-only hand
    temphand=[(rank,suit) for rank,suit in handinfo.hand if rank in ROYAL]

    #case 1: 4 royals, all same suit, so outlier is discarded
    if len(temphand)==4 and len({suit for rank, suit in temphand}) == 1: 
        out=True
        handinfo.discards = [pos for pos,(rank,suit) in enumerate(handinfo.hand) if rank not in ROYAL]

    #case 2: all royals and 4 are same, find the outlying suit           
    elif len(temphand)==5 and 4 in handinfo.countsuit.values():
        badsuit=next(suit for suit,count in handinfo.countsuit.items() if count==1)
        handinfo.discards = [pos for pos,(rank,suit) in enumerate(handinfo.hand) if suit == badsuit]
        out=True

    return(out)


def partial_w0_3ofroyalflush(handinfo: "DWpokerinfo")->bool:
    """
    Check if a hand with 0 wilds contains exactly 3 cards to a Royal Flush.
    Record discards in handinfo.
    Assumes: 0 wild cards
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False

    mxcountsuit=max(handinfo.countsuit.values())
    if mxcountsuit>=3: #3 in flush
        goodsuit=next(suit for suit,count in handinfo.countsuit.items() if count==mxcountsuit)
        #goodsuit=list(handinfo.countsuit.keys())[list(handinfo.countsuit.values()).index(mxcountsuit)]
        #is royal?
        temphand=[(rank,suit) for rank,suit in handinfo.hand if rank in ROYAL and suit==goodsuit]
        if len(temphand)==3:
            out=True
            #handinfo=creatediscards(handinfo.hand, lambda rank,suit: (rank,suit) not in temphand)
            handinfo.discards=[pos for pos,(rank,suit) in enumerate(handinfo.hand) if (rank,suit) not in temphand]
            #handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if not((rank,suit) in temphand)]
    return(out)


def partial_w0_4ofstraightflush(handinfo: "DWpokerinfo")->bool: #Four-card straight flush (open-ended or with a gap)
    """
    Check if a hand with 0 wilds contains exactly 4 cards to a Straight (non-Royal) Flush.
    Record discards in handinfo.
    Assumes: 0 wild cards, assumes flush has already been tested for
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    #we already test if flush so 4 will be same suit
    if (handinfo.wilds==0) and (4 in handinfo.countsuit.values()):
        #find the outlying suit
        badsuit=next(suit for suit,count in handinfo.countsuit.items() if count==1)
        #make a temporary hand without the outlier so we can test it
        #consists of position in series of cards (RANKLIST), not face value
        temphandnum=[RANKLIST.index(rank) for rank,suit in handinfo.hand if suit!=badsuit]

        #outside straight=span of 3,inside straight=span of 4
        if max(temphandnum)-min(temphandnum)<=4:
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if suit==badsuit]
    return(out)


def partial_w0_3ofstraightflush(handinfo:"DWpokerinfo")->bool: #3 to straight flush
    """
    Check if a hand with 0 wilds contains exactly 3 cards to a Straight (non-Royal) Flush.
    This function does not check for royal flush since A is calculated only as low card.
    Equivalent for rf is calculated elsewhere
    Because 2 is wild, lowest sf hand would be 34567, highest 9TJQK
    Record discards in handinfo.
    Assumes: 0 wild cards, assumes flush has already been tested for
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    
    #find if there are 3 suited cards
    goodsuit=next((suit for suit,count in handinfo.countsuit.items() if count==3),'')
    if goodsuit!='':
        temphandnum=[RANKLIST.index(rank) for rank,suit in handinfo.hand if suit==goodsuit]
        
        #if the suited cards are within span of 4, possible straight
        #span of 2=osf, span of 3=isf 1 gap,span of 4=isf 2 gap
        if max(temphandnum)-min(temphandnum)<=4:
            out=True
            handinfo.discards=[pos for pos,(rank,suit) in enumerate(handinfo.hand) if suit!=goodsuit]
            
    return(out)


def partial_w0_4offlush(handinfo:"DWpokerinfo")->bool:
    """
    Check if a hand with 0 wilds contains exactly 4 cards to a Flush.
    Royal Flush had previously been tested
    Record discards in handinfo.
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    
    #test no wild, and 4 are same suit
    if handinfo.wilds==0 and(4 in handinfo.countsuit.values()):
        out=True
        #find the outlier
        badsuit=next(suit for suit,count in handinfo.countsuit.items() if count==1)
        handinfo.discards=[pos for pos,(rank,suit) in enumerate(handinfo.hand) if suit==badsuit]
        #handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if suit==badsuit]
    return(out)


def partial_w0_4ofoutsidestraight(handinfo:"DWpokerinfo")->bool:
    """
    Check if a hand with 0 wilds contains exactly 4 cards to a outside straight.
    This will be 4 consecutive ranks
    A can be low or high
    Record discards in handinfo.
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    
    #make sure all ranks different
    if handinfo.wilds==0 and \
       len(set(handinfo.allrank))==5:
    
        #Special Case: A is high card
        #if A in hand, must have J,Q,K and missing T for outside straight
        #if we consider A to be low, hand wild have '2' which is wild and this will have 0 wilds
        if 'A' in handinfo.allrank:
            #make sure we only look for royals
            temphand=[rank for rank in handinfo.allrank if rank in ROYAL]
            #if we have royals except T
            if len(temphand)==4 and not('T' in temphand):
                #handinfo.discards=[handinfo.allrank.index(list(set(handinfo.allrank)-set(ROYAL))[0])]
                handinfo.discards=[pos for pos,(rank,suit) in enumerate(handinfo.hand) if rank not in ROYAL]
                return True
        #General Case: no A in hand         
        else:
            ranknumlist=[RANKLIST.index(rank) for rank in handinfo.allrank]
            #remove possible outlier, either highest or lowest
            #if there are eactly 4 cards remaining
            #and the span between remaining is exactly 3

            #Case 1: outlier will be higher
            maxcardpos=ranknumlist.index(max(ranknumlist))
            handwohi=[rank for pos,rank in enumerate(ranknumlist) if pos!=maxcardpos]
            if len(set(handwohi))==4 and \
               (max(handwohi)-min(handwohi))==3:
                handinfo.discards=[maxcardpos]
                return True
            
            #Case 2: outlier will be lower
            mincardpos=ranknumlist.index(min(ranknumlist))
            handwolo=[rank for pos,rank in enumerate(ranknumlist) if pos!=mincardpos]
            if len(set(handwolo))==4 and \
               (max(handwolo)-min(handwolo))==3:
                handinfo.discards=[mincardpos]
                return True
    return(out)


def partial_w0_4ofinsidestraight(handinfo:"DWpokerinfo")->bool:
    """
    Check if a hand with 0 wilds contains exactly 4 cards to a inside straight.
    This will be 4 ranks with 1 missing in middle, flush checked elsewhere
    A can be low or high
    Record discards in handinfo.
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    
    #make sure all ranks different
    if handinfo.wilds==0 and \
       len(set(handinfo.allrank))==5:
    
        #Special Case: A in hand to be high, then will be royal
        #if royal, must have T to be inside missing
        #so, it's a non-royal that's an outlier
        if 'A' in handinfo.allrank and 'T' in handinfo.allrank and \
           len(set(handinfo.allrank)-set(ROYAL))==1: 
            out=True
            handinfo.discards=[pos for pos,(rank,suit) in enumerate(handinfo.hand) if rank not in ROYAL]
        #General case: No A
        else:
            #so outlier must be higher or lower than span    
            #make temphand with the ranking of the cards
            tempranknum=[RANKLIST.index(rank) for rank in handinfo.allrank]
            #remove possible outlier, either highest or lowest
            #if there are eactly 4 cards remaining
            #and the span between remaining is exactly 4

            #Case 1: outlier will be higher
            maxcardpos=tempranknum.index(max(tempranknum))
            handwohi=[rank for pos,rank in enumerate(tempranknum) if pos!=maxcardpos]
            if (max(handwohi)-min(handwohi))==4:
                handinfo.discards=[maxcardpos]
                return True
            
            #Case 2: outlier will be lower
            mincardpos=tempranknum.index(min(tempranknum))
            handwolo=[rank for pos,rank in enumerate(ranknumlist) if pos!=mincardpos]
            if (max(handwolo)-min(handwolo))==4:
                handinfo.discards=[mincardpos]
                return True
    return(out)
