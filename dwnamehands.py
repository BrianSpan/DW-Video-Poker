from dwconstants import *

########
# Hand identifying function
########

def namehand(handinfo)->int:    
    if is_w0_royalflush(handinfo): score=NATROYALFLUSH
    elif handinfo.wilds==4: score=FOURWILD
    elif is_wild_royalflush(handinfo): score=WILDROYALFLUSH
    elif is_wild_fivekind(handinfo): score=FIVEKIND
    elif is_straightflush(handinfo): score=STRAIGHTFLUSH
    elif is_w0_fourkind(handinfo) or is_wild_fourkind(handinfo):score=FOURKIND
    elif is_wild_fullhouse(handinfo) or is_w0_fullhouse(handinfo): score=FULLHOUSE
    elif is_wild_flush(handinfo):score=FLUSH
    elif is_straight(handinfo): score=STRAIGHT
    elif is_threekind(handinfo): score=THREEKIND
    elif is_twopair(handinfo): score=TWOPAIR
    elif is_pairjacks(handinfo): score=PAIRJACK
    elif is_pair(handinfo): score=PAIR    
    else: score=JUNK    
    return(score)


##########
# Hand definitions
##########
def is_w0_royalflush(handinfo)->bool: #No wilds royal flush
    out=(handinfo.wilds==0 and
         is_w0_flush(handinfo) and
         is_w0_allroyal(handinfo)
        )
    return(out)


def is_wild_royalflush(handinfo)->bool:#wild royal flush
    out=False
    if (handinfo.wilds>0 and #wild
       set(handinfo.nowildranks).issubset(set(ROYAL)) and #royal
       (len(set(handinfo.nowildsuits))==1) #flush
       ):
        out=True
    return(out)


def is_w0_flush(handinfo)->bool: #no wild flush
    return(len(handinfo.countsuit)==1)


def is_wild_flush(handinfo)->bool: #flush with wildcards
    return(len(set(handinfo.nowildsuits))==1)


def is_wild_fivekind(handinfo)->bool: # wild five of a kind
    #have to have a wild to make 5 of a kind
    #will not have 4 wild because that was evaluated previously
    return(len(set(handinfo.nowildranks))==1)


def is_straightflush(handinfo)->bool: #straight flush with or without wild
    out=False
    if (len(set(handinfo.nowildsuits))==1):#flush
        tmprnk=[RANKLIST.index(rank)
                for rank in handinfo.nowildranks]
        if (len(set(tmprnk))==len(tmprnk) and #are all cards different
           (max(tmprnk)-min(tmprnk)<=4)): #is the span within 5 cards?
            out=True  
    return(out)

def is_w0_fourkind(handinfo)->bool: #natural 4 of kind
    out=False
    #we already tested for 5 of kind
    if handinfo.wilds==0 and (4 in handinfo.countrank.values()):
        badcard=[rank for rank,count in handinfo.countrank.items() if count==1][0]
        handinfo.discard=[handinfo.hand.index((rank,suit)) for (rank,suit) in handinfo.hand if rank==badcard]
        out=True
    return(out)    

def is_wild_fourkind(handinfo)->bool:#wild four of a kind
    #5 of kind already evaluated
    out=False
    if handinfo!=0:
        rnks={rank:handinfo.nowildranks.count(rank) for rank in set(handinfo.nowildranks)} #count all the ranks
        goodcard=[rank for rank,count in rnks.items() if count==4-handinfo.wilds] #check if, with wilds, will have 4 of a rank
        if (len(goodcard)==1):
            out=True
            handinfo.discard=[handinfo.hand.index(card) for card in handinfo.hand if card[0]!=goodcard[0] and card[0]!=WILD]
    return(out) # should be count of 1 or 0


def is_wild_fullhouse(handinfo)->bool:#only valid fh has 1 wild
    #we've already eliminated 4kind
    out=False
    if handinfo.wilds==1:#if a wild, must have 2 pr
        pairs=[rank for rank in set(handinfo.nowildranks)
               if handinfo.nowildranks.count(rank)==2]
        out=(len(pairs)==2)
    return(out)


def is_w0_fullhouse(handinfo)->bool:#no wild, full house
    out=False
    if handinfo.wilds==0 and is_pair(handinfo) and is_w0_threekind(handinfo):
        out=True
    return(out)


def is_straight(handinfo)->bool: #straight, wild or not
    out=False
    if ('A' in handinfo.nowildranks): #if it's Ace, could be low or high
        if (norepeatslst(handinfo.nowildranks)) and \
           (set(handinfo.nowildranks).issubset(set(ROYAL))):
            out=True
    else:          
        tmpranks=[RANKLIST.index(rank)
                  for rank in handinfo.nowildranks]
        if norepeatslst(tmpranks):
            if (max(tmpranks)-min(tmpranks)<=4): #sequence cannot be 4 or more
                out=True  
    return(out)


def is_threekind(handinfo)->bool: 
    out=False
    if is_w0_threekind(handinfo) or is_wild_threekind(handinfo):
        out=True
    return (out)


def is_wild_threekind(handinfo)->bool:
    out=False
    if handinfo.wilds==1: #has to be a pair 
        if 2 in handinfo.countrank.values():#but only 1 pair, else it's fullhouse
            if 1=={counts:(list(handinfo.countrank.values())).count(counts)
                   for counts in set(handinfo.countrank.values())}[2]: #find which has 2
                out=True
                #if needed
                goodrank=list(handinfo.countrank.keys())[list(handinfo.countrank.values()).index(2)]
                handinfo.discards=[handinfo.hand.index((rank,suit))
                          for rank,suit in handinfo.hand
                          if rank!=WILD and rank!=goodrank]
    elif handinfo.wilds==2:
        if len(set(handinfo.nowildranks))==3:#these are 3 singletons
            out=True
            #if needed
            #keep only 1st
            handinfo.discards=[handinfo.hand.index((rank,suit))
                      for rank,suit in handinfo.hand
                      if rank!=WILD and rank!=handinfo.nowildranks[0]]
    #if wilds == 3 or more, then higher hand that we previously tested    
    return(out)


def is_w0_threekind(handinfo)->bool:
    out=False
    if handinfo.wilds==0:
        if 3 in handinfo.countrank.values():
            out=True
            goodranks=list(handinfo.countrank.keys())[list(handinfo.countrank.values()).index(3)]
            handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if rank!=goodranks]
    return(out)


def is_twopair(handinfo)->bool: #Any pair throw away a second pair, if present
    out=False
    if handinfo.wilds==0: #only way to make 2pr is with no wild
        tmprank=[rank for rank,suit in handinfo.hand]
        pairs=[rank for rank in set(tmprank) if tmprank.count(rank)==2]
        if len(pairs)==2:#we determine if there are 2 pairs ...
            out=True
            # Some advice for DW say to discard second pair
            # but we will keep for now
            handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if not(rank in pairs)]
    return (out)


def is_pairjacks(handinfo)->bool:
    out=False
    if 2 in handinfo.countrank.values():
        pairrank=list(handinfo.countrank.keys())[list(handinfo.countrank.values()).index(2)]
        if is_pair(handinfo) and (pairrank in HIGHCARDS):
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit)) for rank,suit in handinfo.hand if rank!=pairrank]
    return(out)


def is_pair(handinfo)->bool:
    out=False
    if handinfo.wilds==0:
        pairs=[rank
               for rank in set(handinfo.allrank)
               if handinfo.allrank.count(rank)==2]
        if len(pairs)==1:
            out=True
            handinfo.discards=[handinfo.hand.index((rank,suit))
                      for rank,suit in handinfo.hand
                      if not(rank==pairs[0])]
    elif handinfo.wilds==1:#all 4 different
        if len(set(handinfo.nowildranks))==4:
            out=True
            #pick one, or we could make pos 0 
            pick=list(handinfo.countrank.keys())[list(handinfo.countrank.values()).index(1)]
            handinfo.discards=[handinfo.hand.index((rank,suit))
                      for rank,suit in handinfo.hand
                      if rank!=WILD and rank!=pick]
    return (out)


#########
# Auxiliary functions
#########

def is_w0_allroyal(handinfo)->bool:
    return(sorted(set(handinfo.allrank))==sorted(ROYAL))


def norepeatslst(inlist:list)-> bool:
    return(len(set(inlist))==len(inlist))
