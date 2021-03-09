import logging
from card import Card
from card_value import CardValue
from poker_hand_value import PokerHandValue

class PokerHand(object):
    def __repr__(self): return self.handStr

    def __init__(self, handStr):
        self.handStr = handStr
        self.handOfCards = []
        self._logger = logging.getLogger(__name__)

        #_logger = logging.getLogger(__name__)
        #self._logger.debug("PokerHand init: " + handStr)

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

        # Sequence:
        # - Straight
        # - Straight flush
        # - Royal Flush

        # Same suit:
        # - Flush
        # - Straight Flush
        # - Royal Flush

        # Sort by value, highest first (ace high)
        self.handOfCards = sorted(self.handOfCards, key=lambda card: card.get_value(), reverse=True)

        highest_card = None
        first_seen_suit = None
        all_same_suit = True
        previous_card = None
        all_in_sequence = True
        cardCounter = {}
        for card in self.handOfCards:
            if not highest_card:
                # List is already sorted, effectively just get the first card
                highest_card = card.get_value()
            if not first_seen_suit:
                first_seen_suit = card.get_suit()

            # Keep track of cards with same value
            if card.get_value() in cardCounter:
                cardCounter[card.get_value()] = cardCounter[card.get_value()] + 1 
            else:
                cardCounter[card.get_value()] = 1

            if card.get_suit() != first_seen_suit:
                all_same_suit = False

            if previous_card:
                if (previous_card.get_value() - card.get_value()) != 1:
                    all_in_sequence = False
            previous_card = card

        matching_card_count = sorted(cardCounter.values(), reverse=True)
        if matching_card_count == [2, 1, 1, 1]:
            self.handValue = PokerHandValue.Pair
        elif matching_card_count == [2, 2, 1]:
            self.handValue = PokerHandValue.TwoPairs
        elif matching_card_count == [3, 1, 1]:
            self.handValue = PokerHandValue.ThreeOfAKind
        elif matching_card_count == [4, 1]:
            self.handValue = PokerHandValue.FourOfAKind
        elif matching_card_count == [3, 2]:
            self.handValue = PokerHandValue.FullHouse
        elif matching_card_count == [1, 1, 1, 1, 1]:
            if all_same_suit:
                if all_in_sequence:
                    if highest_card == CardValue.Ace:
                        self.handValue = PokerHandValue.RoyalFlush
                    else:
                        self.handValue = PokerHandValue.StraightFlush
                else:
                    self.handValue = PokerHandValue.Flush
            elif all_in_sequence:
                self.handValue = PokerHandValue.Straight
        else:
            raise Exception("Unexpected card combination!")
