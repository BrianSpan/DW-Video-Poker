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
        elif partial_w2_4towildroyalflush(handinfo):
            pass  #discards have already been calculated
        elif partial_w2_4tostraightflushexcept(handinfo):
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
        elif partial_w1_4toroyalflush(handinfo):
            pass  #discards have already been calculated
        elif is_wild_fullhouse(handinfo): #fullhouse   #wizardofodds.com
            pass  #discards have already been calculated
        elif is_wild_flush(handinfo): #flush www.888casino.com
            pass  #discards have already been calculated
        elif partial_w1_4tooutsidestraightflush(handinfo): #4 to Straight Flush, 3 consecutive cards, 567 and higher #casino.guru
            pass  #discards have already been calculated 
        elif is_straight(handinfo): #ST   888casino.com
            #straight function already includes wild or not
            pass  #discards have already been calculated
        elif is_wild_threekind(handinfo):
            pass  #discards have already been calculated
        elif  partial_w1_4toinsidestraightflush(handinfo):# 4 ISF, 4 low or higher. www.888casino.com
            pass  #discards have already been calculated
        elif partial_w1_3toroyalflush(handinfo): #3 to Royal Flush
            pass  #discards have already been calculated
        elif partial_w1_3tostraightflush(handinfo):  #3 to Straight Flush, 2 consecutive cards, 67 and higher
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


##########
# Partial hand functions
#
# Recognize a pattern in partial hands
#
##########
######
#
# wilds=1
#
######
def partial_w1_4toroyalflush(handinfo)->bool:#1 wild, all the suited 2 or more royal
    #We previously check WRF (Wild -Royal-Royal-Royal-Royal)
    #WRF with only 1 wild is Wild-Royal-Royal-Royal-unrelated (royals same suit)
    out=False
    #examining the version on the hand with no wilds,
    #must have 3 or 4 Royals
    #if 3, remove unrelated and check all are same suit
    #if 4, unrelated is Royal but different suit
    countroyal=sum(rank in ROYAL for (rank,suit) in handinfo.nowildhand)
    if countroyal==3:
        temphandroyalsinhand=[suit for (rank,suit) in handinfo.nowildhand if rank in ROYAL]
        if len(set(temphandroyalsinhand))==1:
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit))
                               for rank,suit in handinfo.hand
                               if rank!=WILD and not(rank in ROYAL)]
    elif countroyal==4:
        #find which is non-matching suit
        suitcount={suit:handinfo.allsuit.count(suit) for rank,suit in handinfo.nowildhand}
        goodsuit=next((suit for suit,cnt in suitcount.items() if cnt==3),None)
        if goodsuit:
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit))
                               for rank,suit in handinfo.hand
                               if rank!=WILD and suit!=goodsuit]
    return(out)    


def partial_w1_4tooutsidestraightflush(handinfo)->bool:
    #1 wild, 4 to an outside sf, (5-7) or higher
    out=False
    counttempsuit={suit:handinfo.nowildsuits.count(suit)
                   for suit in set(handinfo.nowildsuits)}#count of temp suits
    if 3 in counttempsuit.values():#1 wild + 3 of same suit=near flush
        #find what the suit is and see if straight
        #not 4 because we previously test for flush
        goodsuit=next(suit for suit,count in counttempsuit.items() if count==3)
        #goodsuit=list(counttempsuit.keys())[list(counttempsuit.values()).index(3)]
        smallrankhand=[RANKLIST.index(rank)
                       for rank,suit in handinfo.hand
                       if rank!=WILD and suit==goodsuit]
        minrank=min(smallrankhand)
        maxrank=max(smallrankhand)
        if maxrank-minrank<=3 and minrank>=RANKLIST.index('5'): #outside straight and min 5 or higher
            #find the outlier
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit))
                               for rank,suit in handinfo.hand
                               if rank!=WILD and suit!=goodsuit] 
    return(out)


def partial_w1_4toinsidestraightflush(handinfo)->bool: # 4 ISF, 4 low or higher
    out=False
    if handinfo.wilds==1:
        counttempsuit={suit:handinfo.nowildsuits.count(suit) for suit in set(handinfo.nowildsuits)}
        if 3 in counttempsuit.values():
            #has to be 3, 4 would be flush which we previously test
            badsuit=next(suit for suit,count in counttempsuit.items() if count==1)
            #badsuit=list(counttempsuit.keys())[list(counttempsuit.values()).index(1)]
            temprank=[RANKLIST.index(rank) for rank,suit in handinfo.nowildhand if suit!=badsuit]
            minrank=min(temprank)
            maxrank=max(temprank)
            #is it ISF
            if maxrank-minrank<=4:
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit))
                                   for rank,suit in handinfo.hand
                                   if rank!=WILD and suit==badsuit]
    return(out)


def partial_w1_3toroyalflush(handinfo)->bool: #13. 3 WRF
    out=False
    if handinfo.wilds==1: #1 wild
        smallhand=[(rank,suit)
                   for rank,suit in handinfo.nowildhand
                   if rank in ROYAL]#royal
        if len(set(smallhand))==2: #2 royal + 1 wild = 3 toward
            goodsuit=set([suit for rank,suit in smallhand])
            if len(goodsuit)==1:#flush
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit))
                                   for rank,suit in handinfo.hand
                                   if rank!=WILD and
                                    (suit!=list(goodsuit)[0]
                                      or not(rank in ROYAL))]
    return(out)


def partial_w1_3tostraightflush(handinfo)->bool: #3 to a straight flush with 2 consecutive singletons, #6-7 or higher
    out=False
    
    tempsuitcount={suit:handinfo.nowildsuits.count(suit) for suit in set(handinfo.nowildsuits)}
    if 3 in tempsuitcount.values(): #extra card may be same suit
        #find flush suit
        goodsuit=next(suit for suit,count in tempsuitcount.items() if count==3)
        #goodsuit=list(tempsuitcount.keys())[list(tempsuitcount.values()).index(3)]
        ranks=[RANKLIST.index(rank)
                  for rank,suit in handinfo.nowildhand
                  if suit==goodsuit]
        if max(ranks)-min(ranks)<=4:
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit))
                      for rank,suit in handinfo.hand
                      if rank!=WILD and suit!=goodsuit]
        else: #something in same suit but 2 of sf
            #find outlier and remove
            mincard=min(ranks)
            maxcard=max(ranks)
            nomintemphand=[card for card in ranks if card!=mincard]
            nomaxtemphand=[card for card in ranks if card!=maxcard]
            if max(nomaxtemphand)-min(nomaxtemphand)==1:
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit))
                          for rank,suit in handinfo.hand
                          if rank!=WILD and
                             (suit!=goodsuit or(suit==goodsuit and rank==RANKLIST[maxcard]))]
            elif max(nomintemphand)-min(nomintemphand)==1:
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit))
                          for rank,suit in handinfo.hand
                          if rank!=WILD and
                             (suit!=goodsuit or(suit==goodsuit and rank==RANKLIST[mincard]))]
    elif 2 in tempsuitcount.values():
        goodsuit=next(suit for suit,count in tempsuitcount.items() if count==2)
        #goodsuit=list(tempsuitcount.keys())[list(tempsuitcount.values()).index(2)]
        ranks=[RANKLIST.index(rank)
               for rank,suit in handinfo.nowildhand
               if suit==goodsuit]
        if max(ranks)-min(ranks)==1:
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit))
                               for rank,suit in handinfo.hand
                               if rank!=WILD and suit!=goodsuit]
    return(out)


######
#
# wilds=2
#
######
def partial_w2_4towildroyalflush(handinfo: "DWpokerinfo")->bool: #2W + 2Royal(suited) = 4 to wild royal flush
    """
    Check if 2 deuces + 2 royals (suited) = 4 to a Wild Royal Flush.

    Assumes:
        hand has already been excluded to have only 2 wilds

    Input:
        handinfo - dataclass containing handinfo

    Return:
      bool if the pattern is satisfied

    Changes:
        handinfo.discards - position(0-based) of non-pattern matching card
    """

    out=False

    #partial hand containing only royals
    temphand=[(rank,suit) for rank,suit in handinfo.nowildhand if rank in ROYAL]

    #how many royals are there?
    #Case 1: Exactly 2 royals, check if same suit
    if len(temphand)==2: #how many royals are there?
        #same suit? then drop the outlier
        goodsuit=list(set([suit for (rank,suit)in temphand]))
        if len(goodsuit)==1: #only 1 suit
            out=True
            handinfo.discards=[cardpos
                               for cardpos, (rank, suit) in enumerate(handinfo.hand)
                               if rank != WILD
                               #for cardpos in range(5)
                               #if (rank:=handinfo.hand[cardpos][0])!=WILD
                               and not rank in ROYAL]

    # Case 2: Exactly 3 royals, 2 in suit and 1 outlier
    elif len(temphand)==3: #if 3 royals, then how many suits?
        #suits=[suit for rank,suit in temphand]
        #countsuits={suit:suits.count(suit) for suit in set(suits)}
        countsuits = Counter(suit for rank,suit in temphand)
        if len(countsuits)==2: #if 2 suits, remove the outlier
            out=True
            #remove the outlier
            badsuit=next(suit for suit,count in countsuits.items() if count==1)
            #badsuit=list(counttsuits.keys())[list(counttsuits.values()).index(1)]
            handinfo.discards=[cardpos
                               #for cardpos in range(5)
                               for cardpos, (rank, suit) in enumerate(handinfo.hand)
                               #if (rank:=handinfo.hand[cardpos][0])!=WILD
                               #and (suit:=handinfo.hand[cardpos][1])==badsuit
                               if rank != WILD and suit == badsuit
                               ]
    return(out)

def partial_w2_4tostraightflushexcept(handinfo):
    #different sources describe it as:
    #4 to a straight flush with 2 consecutive singletons, 6-7 or higher
    #4 to Straight Flush 2 suited, consecutive cards, 67 and higher
    #Any suited, consecutive, two-card sequence except: (3,4), (4,5) or (5,6)
    out=False
    #find the matching suit
    countsuits={suit:handinfo.nowildsuits.count(suit) for suit in set(handinfo.nowildsuits)}
    if len(countsuits)==2:#out of 3 cards if 2 are same suit, '2'
        badsuit=next(suit for suit,count in countsuits.items() if count==1)
        #badsuit=list(countsuits.keys())[list(countsuits.values()).index(1)]#''suited'
        #are the remaining cards consecutive
        temphand=[RANKLIST.index(rank) for rank,suit in handinfo.hand if rank!=WILD and suit!=badsuit]
        if abs(temphand[1]-temphand[0])==1:#'consecutive'
            if min(temphand)>=RANKLIST.index('6'):
            #6-7 or higher
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if suit==badsuit and rank!=WILD]
    
    return(out)    

