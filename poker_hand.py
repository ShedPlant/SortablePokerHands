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
            self.set_hand_value()
        except:
            raise Exception("One or more cards invalid!")

        self._logger.debug(self.describe())
    
    def describe(self):
        desc = "Poker Hand: " + self.handStr + ": " + self.handValue.name
        #for card in self.handOfCards:
            #desc += "\n - "
            #desc += card.describe()
        #desc += "\nValue: " + self.handValue.name
        return desc

    def get_value(self):
        return self.handValue

    def set_hand_value(self):
        # TODO remove stub
        self.handValue = PokerHandValue.HighCard

        # At least two cards the same:
        # - Pair
        # - Two Pairs
        # - Three of a Kind
        # - Full House
        # - Four of a Kind
        numCardsSameValue = 1

        # Sequence:
        # - Straight
        # - Straight flush
        # - Royal Flush
        straight = False

        # Same suit:
        # - Flush
        # - Straight Flush
        # - Royal Flush
        flush = False

        # Sort by value, highest first (ace high)
        #self._logger.debug(self.handOfCards)
        #for card in self.handOfCards: print(card.get_value())
        self.handOfCards = sorted(self.handOfCards, key=lambda card: card.get_value())
        #self._logger.debug(self.handOfCards)
        #for card in self.handOfCards: print(card.get_value())

        highestCard = None
        firstSeenSuit = None
        cardCounter = {}
        for card in self.handOfCards:
            if not highestCard:
                # List is already sorted, effectively just get the first card
                highestCard = card.get_value()
            if not firstSeenSuit:
                firstSeenSuit = card.get_suit()
            
            if card.get_value() in cardCounter:
                cardCounter[card.get_value()] = cardCounter[card.get_value()] + 1 
            else:
                cardCounter[card.get_value()] = 1

        matchingCardCount = sorted(cardCounter.values(), reverse=True)
        self._logger.debug("matchingCardCount: " + str(matchingCardCount))
        if matchingCardCount == [2, 1, 1, 1]:
            self.handValue = PokerHandValue.Pair
        elif matchingCardCount == [2, 2, 1]:
            self.handValue = PokerHandValue.TwoPairs
        elif matchingCardCount == [3, 1, 1]:
            self.handValue = PokerHandValue.ThreeOfAKind
        elif matchingCardCount == [4, 1]:
            self.handValue = PokerHandValue.FourOfAKind
        elif matchingCardCount == [3, 2]:
            self.handValue = PokerHandValue.FullHouse