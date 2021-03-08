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
        # TODO work out hand value
        # algorithm
        # could have a function one at a time 'is it a royal flush etc'
        #
        # sort cards by value / suit ?
        # probably more efficient to look at each card and rule in (or out?)
        # possible combinations
        #sorted_cards_by_value = sorted(self.handOfCards, key=lambda card: card.value)
        #self._logger.debug("sorted cards: " + sorted_cards_by_value)





