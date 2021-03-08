import logging
from card import Card
from poker_hand_value import PokerHandValue

class PokerHand(object):
    def __repr__(self): return self.handStr

    def __init__(self, handStr):
        self.handStr = handStr
        self.handOfCards = []
        self._logger = logging.getLogger(__name__)

        #_logger = logging.getLogger(__name__)
        self._logger.debug("PokerHand init: " + handStr)

        handStrList = handStr.split()
        if len(handStrList) != 5:
            raise Exception("Hand must contain 5 cards!")
        if list(dict.fromkeys(handStrList)) != handStrList:
            raise Exception("Hand cannot contain duplicate cards!")

        try:
            for cardStr in handStrList:
                self.handOfCards.append(Card(cardStr))
        except:
            raise Exception("One or more cards invalid!")

        self.set_hand_value()

        self._logger.debug(self.describe())
    
    def describe(self):
        desc = "Poker Hand: " + self.handStr
        for card in self.handOfCards:
            desc += "\n - "
            desc += card.describe()
        desc += "\nValue: " + self.handValue.name
        return desc

    def get_value(self):
        return self.handValue

    def set_hand_value(self):
        self.handValue = PokerHandValue.HighCard
        # At least two cards the same:
        # - Pair
        # - Two Pairs
        # - Three of a Kind
        # - Full House
        # - Four of a Kind

        # Sequence:
        # - Straight
        # - Straight flush
        # - Royal Flush

        # Same suit:
        # - Flush
        # - Straight Flush
        # - Royal Flush

        # Sort by value, highest first (ace high)
        #self._logger.debug(self.handOfCards)
        #for card in self.handOfCards: print(card.get_value())
        self.handOfCards = sorted(self.handOfCards, key=lambda x: x.get_value())
        #self._logger.debug(self.handOfCards)
        #for card in self.handOfCards: print(card.get_value())






