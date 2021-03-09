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
        desc = "Poker Hand: " + self.handStr + ": " + self.hand_value.name
        #for card in self.handOfCards:
            #desc += "\n - "
            #desc += card.describe()
        #desc += "\nValue: " + self.hand_value.name
        return desc

    def get_value(self):
        return self.hand_value

    # Compare by hand value
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.get_value() < other.get_value()
        return NotImplemented

    def set_hand_value(self):
        # Sort by value, highest first (ace high)
        self.handOfCards = sorted(self.handOfCards, key=lambda card: card.get_value(), reverse=True)

        highest_card = None
        first_seen_suit = None
        all_same_suit = True
        previous_card = None
        num_in_sequence = 1
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
                # Cards are adjacent e.g. 3 and 4
                if (previous_card.get_value() - card.get_value()) == 1:
                    num_in_sequence = num_in_sequence + 1

                # Special case, low ace adjacent to 2
                if card.get_value() == CardValue.Two and highest_card == CardValue.Ace:
                    num_in_sequence = num_in_sequence + 1

            previous_card = card

        if num_in_sequence != 5:
            all_in_sequence = False

        matching_card_count = sorted(cardCounter.values(), reverse=True)
        if matching_card_count == [2, 1, 1, 1]:
            self.hand_value = PokerHandValue.Pair
        elif matching_card_count == [2, 2, 1]:
            self.hand_value = PokerHandValue.TwoPairs
        elif matching_card_count == [3, 1, 1]:
            self.hand_value = PokerHandValue.ThreeOfAKind
        elif matching_card_count == [4, 1]:
            self.hand_value = PokerHandValue.FourOfAKind
        elif matching_card_count == [3, 2]:
            self.hand_value = PokerHandValue.FullHouse
        elif matching_card_count == [1, 1, 1, 1, 1]:
            if all_same_suit:
                if all_in_sequence:
                    if highest_card == CardValue.Ace:
                        self.hand_value = PokerHandValue.RoyalFlush
                    else:
                        self.hand_value = PokerHandValue.StraightFlush
                else:
                    self.hand_value = PokerHandValue.Flush
            elif all_in_sequence:
                self.hand_value = PokerHandValue.Straight
            else:
                self.hand_value = PokerHandValue.HighCard
        else:
            raise Exception("Unexpected card combination!")
