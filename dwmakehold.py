from dwconstants import *
from dwnamehands import *

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
            badcard=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if handinfo.nowildranks.count(rank)==1][0]
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
        elif partial_w0_3toroyalflush(handinfo):#3 to a royal flush
            pass  #discards have already been calculated
        elif partial_w0_4toflush(handinfo):#4 FL
            pass  #discards have already been calculated
        elif handinfo.handscore==TWOPAIR or handinfo.handscore==PAIRJACK or handinfo.handscore==PAIR:
            pass  #discards have already been calculated
        elif partial_w0_4tooutsidestraight(handinfo):#4 to an outside straight
            pass  #discards have already been calculated
        elif partial_w0_3tostraightflush(handinfo): #3 to straight flush
            pass  #discards have already been calculated
        elif partial_w0_4toinsidestraight(handinfo):#4 to an inside straight, except missing deuce
            pass  #discards have already been calculated
        else:#junk
            handinfo.discards=list(range(5)) #all 5
        
    out=[not(cardindex in handinfo.discards) for cardindex in range(5)]    
    return(out)


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
def partial_w0_4ofroyalflush(handinfo)->bool:
    out=False
        
    if handinfo.wilds==0:
        #make a hand to see if there are royals
        temphand=[(rank,suit)
                  for rank,suit in handinfo.hand
                  if rank in ROYAL]
        if len(temphand)==4:#are all the royals same suit
            tempsuit=[suit for rank,suit in temphand]
            if len(set(tempsuit))==1:
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit))
                          for rank,suit in handinfo.hand
                          if not(rank in ROYAL)]
        elif len(temphand)==5:#find the nonsuited royal
            if 4 in handinfo.countsuit.values():
                out=True
                badsuit=next(suit for suit,count in handinfo.countsuit.items() if count==1)
                #badsuit=list(handinfo.countsuit.keys())[list(handinfo.countsuit.values()).index(1)]
                handinfo.discards=[handinfo.hand.index((rank,suit))
                          for rank,suit in handinfo.hand
                          if suit==badsuit]
    return(out)

def partial_w0_4ofstraightflush(handinfo)->bool: #Four-card straight flush (open-ended or with a gap)
    out=False
    #we already test if flush so 4 will be same suit
    if (handinfo.wilds==0) and (4 in handinfo.countsuit.values()): #4 in a flush
        badsuit=next(suit for suit,count in handinfo.countsuit.items() if count==1)
        #badsuit=list(handinfo.countsuit.keys())[list(handinfo.countsuit.values()).index(1)]
        temphandnum=[RANKLIST.index(rank) for rank,suit in handinfo.hand if suit!=badsuit]
        mn=min(temphandnum)
        mx=max(temphandnum)
        if mx-mn<=4: #outside straight=3 different,inside straight=4 different
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if suit==badsuit]
    return(out)

def partial_w0_3toroyalflush(handinfo)->bool:#3 to a royal flush
    out=False
    mxcountsuit=max(handinfo.countsuit.values())
    if mxcountsuit>=3: #3 in flush
        goodsuit=next(suit for suit,count in handinfo.countsuit.items() if count==mxcountsuit)
        #goodsuit=list(handinfo.countsuit.keys())[list(handinfo.countsuit.values()).index(mxcountsuit)]
        #is royal?
        temphand=[(rank,suit) for rank,suit in handinfo.hand if rank in ROYAL and suit==goodsuit]
        if len(temphand)==3:
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if not((rank,suit) in temphand)]
    return(out)


def partial_w0_4toflush(handinfo)->bool:
    out=False
    if handinfo.wilds==0 and(4 in handinfo.countsuit.values()):
        badsuit=next(suit for suit,count in handinfo.countsuit.items() if count==1)
        #badsuit=list(handinfo.countsuit.keys())[list(handinfo.countsuit.values()).index(1)]
        out=True
        handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if suit==badsuit]
    return(out)

def partial_w0_4tooutsidestraight(handinfo)->bool:# 4 to an outside straight
    out=False
    if handinfo.wilds==0:
        #because A is usually ranked as low card,
        #... we have to break out this exception for royal straight
        if 'A' in handinfo.allrank:
            temphand=[rank for rank in handinfo.allrank if rank in ROYAL]
            #only way to have OUTSIDE rotal straight that includes A is to not have 10
            if len(temphand)==4 and not('T' in temphand):
                out=True
                #find outlier
                handinfo.discards=[handinfo.allrank.index(list(set(handinfo.allrank)-set(ROYAL))[0])]
        else:
            ranknumlist=[RANKLIST.index(rank) for rank in handinfo.allrank]
            #if we remove one of the ends, is it straight?
            mincardpos=ranknumlist.index(min(ranknumlist))
            maxcardpos=ranknumlist.index(max(ranknumlist))
            #outlier will be lower or higher than the rest
            handwohi=ranknumlist.copy()
            del handwohi[maxcardpos]
            handwolo=ranknumlist.copy()
            del handwolo[mincardpos]
            #if we remove the highest, is it ost?
            if len(set(handwohi))==4 and (max(handwohi)-min(handwohi))==3:
                out=True
                handinfo.discards=[maxcardpos]
            #if we remove lowest, is it ost?    
            elif len(set(handwolo))==4 and (max(handwolo)-min(handwolo))==3:
                out=True
                handinfo.discards=[mincardpos]    
    return(out)

def partial_w0_3tostraightflush(handinfo)->bool: #3 to straight flush
    out=False
    ranks=list(handinfo.countsuit.keys())
    rankscount=list(handinfo.countsuit.values())
    if 3 in rankscount: #is 3 to a flush? We alraeady check 4to flush so no need to eliminate
        goodsuit=ranks[rankscount.index(3)]
        temphand=[RANKLIST.index(rank) for rank,suit in handinfo.hand if suit==goodsuit]
        if max(temphand)-min(temphand)<=4:#diff of 2=osf,3=isf 1 gap,4=isf 2 gap
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if suit!=goodsuit]
    return(out)

def partial_w0_4toinsidestraight(handinfo)->bool:#4 to an inside straight
    #Have previously checked outside straight
    out=False
    ranks=[RANKLIST.index(rank) for rank in handinfo.allrank]
    # check if royal ist
    if 'A' in handinfo.allrank and 'T' in handinfo.allrank and \
      len((set(handinfo.allrank)-{'A','T'}).intersection(set(ROYAL)-{'A','T'}))==2:
        out=True
        handinfo.discards=[handinfo.allrank.index(list(set(handinfo.allrank).difference(set(ROYAL)))[0])]
    else:    
        mincardpos=ranks.index(min(ranks))
        maxcardpos=ranks.index(max(ranks))
        #outlier will be lower or higher than the rest
        handwohi=ranks.copy()
        del handwohi[maxcardpos]
        handwolo=ranks.copy()
        del handwolo[mincardpos]
        if len(set(handwohi))==4:
            #if we remove the highest, is it ost?
            if max(handwohi)-min(handwohi)==4 \
                and set(handwohi)!=set([0,2,3,4]): #and missing card is not wild
                out=True
                handinfo.discards=[maxcardpos]
            #if we remove lowest, is it ost?    
            elif max(handwolo)-min(handwolo)==4:
                out=True
                handinfo.discards=[mincardpos]    
    return(out)

######
#
# wilds=1
#
######
def partial_w1_4toroyalflush(handinfo)->bool:#1 wild, all the suited 2 or more royal
    #We previously check WRF (Wild -Royal-Royal-Royal-Royal)
    #WRF with only 1 wild is Wild-Royal-Royal-Royal-unrelated
    out=False
    if handinfo.wilds==1:
        #make a temp hand of only royals
        temproyalhand=[(rank,suit) for rank,suit in handinfo.nowildhand if rank in ROYAL]
        #1 wild so there must be 3 royals, all different, only 1 suit
        if len(temproyalhand)==3 \
           and len(set([rank for rank,suit in temproyalhand]))==3 \
           and len(set([suit for rank,suit in temproyalhand]))==1:
            tempsuit=[suit for rank,suit in temproyalhand]
            counttempsuit={suit:tempsuit.count(suit) for suit in set(tempsuit)}
            #royalsintemp=len(temproyalhand)
            if len(set(tempsuit))==1: #flush
                #find outlier if any - this will be 4 to WRF
                out=True
                handinfo.discards=[handinfo.hand.index((rank,suit))
                                   for rank,suit in handinfo.hand
                                   if rank!=WILD and not(rank in ROYAL)]
        elif len(temproyalhand)==4:
            #there is royal card out of suit
            #all royal but unrelated is different suit
            #what's the distrubution of suits
            counttempsuit={suit: sum(1 for (r1,s1) in temproyalhand if s1==suit)
                           for suit in set(suit for (rank,suit) in temproyalhand)}
            distribsuit=counttempsuit.values()
            if 3 in distribsuit: #we want 3 so throw out outlier
                out=True
                badsuit=next(suit for suit,count in counttempsuit.items() if count==1)
                #badsuit=list(counttempsuit.keys())[list(counttempsuit.values()).index(1)]
                handinfo.discards=[handinfo.hand.index((rank,suit))
                                   for rank,suit in handinfo.hand
                                   if rank in ROYAL and suit==badsuit]
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
def partial_w2_4towildroyalflush(handinfo):
    #2W + 2Royal(suited) = 4 to wild royal flush
    out=False
    temphand=[(rank,suit) for rank,suit in handinfo.nowildhand if rank in ROYAL]
    if len(temphand)==2: #how many royals are there?
        #same suit? then drop the outlier
        goodsuit=list(set([suit for (rank,suit)in temphand]))
        if len(goodsuit)==1:
            out=True
            handinfo.discards=[cardpos
                               for cardpos in range(5)
                               if (rank:=handinfo.hand[cardpos][0])!=WILD
                               and not rank in ROYAL]
    elif len(temphand)==3: #if 3 royals, then how many suits?
        suits=[suit for rank,suit in temphand]
        countsuits={suit:suits.count(suit) for suit in set(suits)}
        if len(countsuits)==2: #if 2 suits, remove the outlier
            out=True
            #remove the outlier
            badsuit=next(suit for suit,count in countsuits.items() if count==1)
            #badsuit=list(counttsuits.keys())[list(counttsuits.values()).index(1)]
            handinfo.discards=[cardpos
                               for cardpos in range(5)
                               if (rank:=handinfo.hand[cardpos][0])!=WILD
                               and (suit:=handinfo.hand[cardpos][1])==badsuit
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

