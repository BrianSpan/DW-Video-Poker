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
    Assumes: 0 wild cards
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False

    #case 1: 4 royals, all same suit, so outlier is discarded
    if len(handinfo.onlyroyal)==4 and len({suit for rank, suit in handinfo.onlyroyal}) == 1:
        out=True
        handinfo.discards = [pos for pos,(rank,suit) in enumerate(handinfo.hand) if rank not in ROYAL]

    #case 2: all royals and 4 are same, find the outlying suit           
    elif len(handinfo.onlyroyal)==5 and 4 in handinfo.countsuit.values():    
        badsuit=next(suit for suit,count in handinfo.countsuit.items() if count==1)
        handinfo.discards = [pos for pos,(rank,suit) in enumerate(handinfo.hand) if suit == badsuit]
        out=True

    return(out)


def partial_w0_3ofroyalflush(handinfo: "DWpokerinfo")->bool:
    """
    Check if a hand with 0 wilds contains exactly 3 cards to a Royal Flush.
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
        #is royal?
        temphand=[(rank,suit) for rank,suit in handinfo.hand if rank in ROYAL and suit==goodsuit]
        if len(temphand)==3:
            out=True
            handinfo.discards=[pos for pos,(rank,suit) in enumerate(handinfo.hand) if (rank,suit) not in temphand]
    return(out)


def partial_w0_4ofstraightflush(handinfo: "DWpokerinfo")->bool: #Four-card straight flush (open-ended or with a gap)
    """
    Check if a hand with 0 wilds contains exactly 4 cards to a Straight (non-Royal) Flush.
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
            #We do not have to worry about A being low because 2 would be wild
            #So lowest non-wild straight is 34567
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

##########
#
# wilds=1
#
##########
def partial_w1_4ofroyalflush(handinfo: "DWpokerinfo")->bool:#1 wild, all the suited 2 or more royal
    """
    Check if a hand with 1 wild contains comination to a Royal Flush.
    We have previously tested "Wild-Royal-Royal-Royal-Royal"
    This tests "Wild-Royal-Royal-Royal-unrelated"
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    if handinfo.wilds==1:
        #examining the version on the hand with no wilds,
        #must have 3 or 4 Royals
        countroyal=len(handinfo.onlyroyal)
        #Case 1: if 3 Royals, remove unrelated and verify all are suited
        if countroyal==3:
            royalssuits=[suit for (rank,suit) in handinfo.onlyroyal]
            if len(set(royalssuits))==1:
                out=True
                handinfo.discards=[pos for pos,(rank,suit) in enumerate(handinfo.hand)
                                   if rank!=WILD and not(rank in ROYAL)]
        #Case 2: if 4 Royals, unrelated is Royal but different suit
        elif countroyal==4:
            #find which is non-matching suit
            suitcount={suit:handinfo.allsuit.count(suit) for rank,suit in handinfo.nowildhand}
            goodsuit=next((suit for suit,cnt in suitcount.items() if cnt==3),None)
            if goodsuit!=None:
                out=True
                handinfo.discards=[pos for pos,(rank,suit)
                                   in enumerate(handinfo.hand)
                                   if rank!=WILD and suit!=goodsuit]
    return(out)    


def partial_w1_3ofroyalflush(handinfo)->bool: #13. 3 WRF
    """
    Check if a hand with 1 wild contains combination to a Royal Flush.
    We have previously tested "Wild-Royal-Royal-Royal-Royal"
    This tests "Wild-Royal-Royal-unrelated-unrelated" (suited royals)
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    
    if handinfo.wilds==1:
        #find the suits in royals-only hand
        royalsuitcount=dict(Counter(suit for rank,suit in handinfo.onlyroyal))
        #what suit contributes to royal flush
        goodsuit=next((suit for suit,count in royalsuitcount.items() if count==2),None)
        if goodsuit!=None:
            #eliminate royal of wrong suit
            smallhand=[(rank,suit)
                   for rank,suit in handinfo.onlyroyal
                   if suit==goodsuit]
            #need exactly 2 royals, different, same suit
            if len(smallhand)==2:
                out=True
                handinfo.discards=[pos for pos,(rank,suit) in enumerate(handinfo.hand)
                                   if rank!=WILD and
                                   (suit!=goodsuit or
                                    rank not in ROYAL)    
                                   ]
    return(out)


def partial_w1_4ofoutsidestraightflush(handinfo:"DWpokerinfo")->bool:
    #1 wild, 4 to an outside sf, (5-7) or higher
    """
    Check if a hand with 1 wild contains a total of
    4 cards to an outside straight flush.
    I.e.: Wild-suited-suited-suited-not
    We previously test for flush (1 wild + 4 suited).
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    if handinfo.wilds==1:
        #find how many are in each suit after wilds
        counttempsuit=Counter(handinfo.nowildsuits)
        if 3 in counttempsuit.values():#3 suited 
            #get matching suit
            goodsuit=next(suit for suit,count in counttempsuit.items() if count==3)
            #make just small (3 cards) suited hand to find lowest and highest card
            smallrankhand=[RANKLIST.index(rank)
                           for rank,suit in handinfo.hand
                           if rank!=WILD and suit==goodsuit]
            minrank=min(smallrankhand)
            maxrank=max(smallrankhand)
            #outlier will be outside a short span
            #span of 2 between min and max means bad is outside
            #low card must be 5 or higher
            if maxrank-minrank<=2 \
               and minrank>=RANKLIST.index('5'):
                #find the outlier
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit))
                                   for rank,suit in handinfo.hand
                                   if rank!=WILD and suit!=goodsuit] 
    return(out)


def partial_w1_4ofinsidestraightflush(handinfo:"DWpokerinfo")->bool:
    #1 wild, 4 to an inside sf, (5-7) or higher
    """
    Check if a hand with 1 wild contains a total of
    4 cards to an outside straight flush.
    I.e.: Wild-suited-suited-suited-not
    We previously test for flush (1 wild + 4 suited).
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    if handinfo.wilds==1:
        #find how many are in each suit after wilds
        counttempsuit=Counter(handinfo.nowildsuits)
        if 3 in counttempsuit.values():#3 suited 
            #get matching suit
            goodsuit=next(suit for suit,count in counttempsuit.items() if count==3)
            #make just small (3 cards) suited hand to find lowest and highest card
            smallrankhand=[RANKLIST.index(rank)
                           for rank,suit in handinfo.hand
                           if rank!=WILD and suit==goodsuit]
            minrank=min(smallrankhand)
            maxrank=max(smallrankhand)
            #outlier will be outside a short span
            #span of 3 between min and max means bad is outside
            #low card must be 5 or higher
            if maxrank-minrank<=3 \
               and minrank>=RANKLIST.index('5'):
                #find the outlier
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit))
                                   for rank,suit in handinfo.hand
                                   if rank!=WILD and suit!=goodsuit] 
    return(out)


def partial_w1_3ofstraightflush(handinfo:"DWpokerinfo")->bool:
    #3 to a straight flush with 2 consecutive singletons, #6-7 or higher
    """
    Check if a hand with 1 wild contains a total of
    3 cards to an straight flush.
    I.e.: Wild-suited-suited-not-not
    Also, eligible cards must be consecutive
    Args:
        handinfo (DWpokerinfo): Object with poker hand details.
    Affects:
        handinfo.discards
    Returns:
        bool:  if conditions met
    """
    out=False
    #find the suits
    tempsuitcount=Counter(handinfo.nowildsuits)
    #case 1: "extra" cards are non-suited
    if 2 in tempsuitcount.values():
        suitswithtwo=[suit for suit,cnt in tempsuitcount.items() if cnt==2]
        #There may be 2 sets of 2 card suit matches
        #go through both sets, accept first if both work
        for goodsuit in suitswithtwo:
            ranks=[RANKLIST.index(rank)
                   for rank,suit in handinfo.nowildhand
                   if suit==goodsuit]
            #consecutive
            if max(ranks)-min(ranks)==1:
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit))
                                   for rank,suit in handinfo.hand
                                   if rank!=WILD and suit!=goodsuit]
                break
    #Case 2: 1 of the "extra" cards is same suit
    #we eliminate a non-consecutive
    #We dont have to check if 4 of same suit since we previouisly checked for flush        
    elif 3 in tempsuitcount.values():
        goodsuit=next(suit for suit,count in tempsuitcount.items() if count==3)
        #make a mini hand of just the 3 in the suit
        tempranksorted=sorted([RANKLIST.index(rank)
                      for rank,suit in handinfo.nowildhand
                      if suit==goodsuit])
        #in a sorted list, consecutive will be 1 different than middle number
        #case2A: outlier is largest
        if tempranksorted[0]==tempranksorted[1]-1:
            badvalue=tempranksorted[2]
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit))
                               for rank,suit in handinfo.hand
                               if (rank!=WILD and suit!=goodsuit)
                               or rank==RANKLIST[badvalue]]
        #case 2b: outlier is smallest
        elif tempranksorted[1]==tempranksorted[2]-1:
            badvalue=tempranksorted[0]
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit))
                               for rank,suit in handinfo.hand
                               if (rank!=WILD and suit!=goodsuit)
                               or rank==RANKLIST[badvalue]]
        #case 2C: there are no consecutive
        #pass
    return(out)


######
#
# wilds=2
#
######
def partial_w2_4ofwildroyalflush(handinfo: "DWpokerinfo")->bool:
    """
    Check if 2 wildcards + 2 royals (suited) + unrelated = 4 to a Wild Royal Flush.
    We've previously eliminated 2 wilds+3 suited royals
    Args:
        handinfo - dataclass containing handinfo
    Return:
        bool if the pattern is satisfied
    Changes:
        handinfo.discards - position(0-based) of non-pattern matching card
    """
    out=False
    if handinfo.wilds==2:
        #how many royals are there?
        #Case 1: Exactly 2 royals, check if same suit
        if len(handinfo.onlyroyal)==2: #how many royals are there?
            countsuit=Counter(suit for rank,suit in handinfo.onlyroyal)
            if len(countsuit)==1:
                #if so...
                goodsuit=next(iter(countsuit))
                #... it's the match we're looking for
                out=True
                handinfo.discards=[cardpos
                                   for cardpos, (rank, suit) in enumerate(handinfo.hand)
                                   if rank != WILD
                                   and suit!=goodsuit
                                   and not rank in ROYAL]
        # Case 2: Exactly 3 royals, 2 in suit and 1 outlier
        elif len(handinfo.onlyroyal)==3: #if 3 royals, then how many suits?
            countsuit = Counter(suit for rank,suit in handinfo.onlyroyal)
            if len(countsuit)==2: #if 2 suits, remove the outlier
                out=True
                #find the outlier
                goodsuit=next(suit for suit,count in countsuit.items() if count==2)
                handinfo.discards=[cardpos
                                   for cardpos, (rank, suit) in enumerate(handinfo.hand)
                                   if rank != WILD
                                   and suit!= goodsuit
                                   ]
    return(out)


def partial_w2_4ofstraightflushexcept(handinfo:"DWpokerinfo")->bool:
    """
    Check if 2 wildcards + 2 consecutive suited = 4 to a Straight Flush.
    6-7 and higher
    Args:
        handinfo - dataclass containing handinfo
    Return:
        bool if the pattern is satisfied
    Changes:
        handinfo.discards - position(0-based) of non-pattern matching card
    """
    #different sources describe it as:
    #4 to a straight flush with 2 consecutive singletons, 6-7 or higher
    #4 to Straight Flush 2 suited, consecutive cards, 67 and higher
    #Any suited, consecutive, two-card sequence except: (3,4), (4,5) or (5,6)
    out=False
    if handinfo.wilds==2:
        #find the matching suit
        countsuits={suit:handinfo.nowildsuits.count(suit) for suit in set(handinfo.nowildsuits)}
        if len(countsuits)==2:#out of 3 cards if 2 are same suit
            badsuit=next(suit for suit,count in countsuits.items() if count==1)
            #are the remaining cards consecutive
            temphand=[RANKLIST.index(rank) for rank,suit in handinfo.hand if rank!=WILD and suit!=badsuit]
            if abs(temphand[1]-temphand[0])==1:#'consecutive'
                if min(temphand)>=RANKLIST.index('6'):
                #6-7 or higher
                    out=True
                    handinfo.discards=[cardpos
                                       for cardpos, (rank, suit) in enumerate(handinfo.hand)
                                       if suit==badsuit and rank!=WILD]    
    return(out)    
