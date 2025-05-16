from dwconstants import *
from dwnamehands import *

#create info about the hand
class DWpokerinfo:
    def __init__(self,hand):
        #temporary to keep track of discards
        self.discards=[]

        #precalculations
        self.hand=hand
        self.allrank =[rank for rank,suit in hand]
        self.countrank={rank:self.allrank.count(rank) for rank in set(self.allrank)}
        self.allsuit =[suit for rank,suit in hand]
        self.countsuit={suit:self.allsuit.count(suit) for suit in set(self.allsuit)}
        self.wilds=self.countrank.get(WILD,0)
        self.nowildhand=[(rank,suit) for rank,suit in hand if rank!=WILD]
        self.nowildranks=[rank for rank,suit in hand if rank!=WILD]
        self.nowildsuits=[suit for rank,suit in hand if rank!=WILD]
        
        #calculate the hand
        self.handscore=namehand(self)