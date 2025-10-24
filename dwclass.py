from dwconstants import *
from dwnamehands import *

#Create info about the hand
class DWpokerinfo:
    def __init__(self, hand: list[tuple[str,str]])->None:
        """
        Initializes an object to hold information on a poker hand including wildcards.

        Args:
            hand (list of tuples): A list of 5 single-character (rank, suit) tuples representing a poker hand.
                Example: [('K', 'H'), ('3', 'D'), ('2', 'D'), ('T', 'S'), ('A', 'S')] *note: T represents 10
        """
        
        #keep track of discards during swapping
        self.discards: list[int] = []
        # original hand
        self.hand = hand

        #precalculations
        # list of ranks
        self.allrank = [rank for rank, suit in hand]
        # Count of each rank
        self.countrank = {rank: (self.allrank).count(rank) for rank in set(self.allrank)}
        # list of suits
        self.allsuit = [suit for rank, suit in hand]
        # Count of each suit
        self.countsuit = {suit: (self.allsuit).count(suit) for suit in set(self.allsuit)}

        # Count of wildcards
        self.wilds = (self.countrank).get(WILD, 0)
        # version of hand without wildcards
        self.nowildhand = [(rank, suit) for rank, suit in hand if rank != WILD]
        #hand with only royals
        self.onlyroyal=[(rank,suit) for rank,suit in self.nowildhand if rank in ROYAL]
        # list of ranks from non-wildcard hand
        self.nowildranks = [rank for rank, suit in hand if rank != WILD]
        # list of suits from non-wildcard hand
        self.nowildsuits = [suit for rank, suit in hand if rank != WILD]
        # Count of each rank in non-wildcard hand
        self.nowildcountrank = {rank: (self.nowildranks).count(rank) for rank in set(self.nowildranks)}
        # Count of each suit in non-wildcard hand
        self.nowildcountsuit = {suit: (self.nowildsuits).count(suit) for suit in set(self.nowildsuits)}

        # Calulate the hand
        self.handscore = namehand(self)  #defined in dwnamehands.py
