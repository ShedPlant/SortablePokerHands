import logging
from card import Card
from card_value import CardValue
from poker_hand_value import PokerHandValue

class PokerHand(object):
    def __repr__(self): return self.handStr

    def __init__(self, handStr):
        self.handStr = handStr
        self._logger = logging.getLogger(__name__)

        #_logger = logging.getLogger(__name__)
        #self._logger.debug("PokerHand init: " + handStr)

        handStrList = handStr.split()
        if len(handStrList) != 5:
            raise Exception("Hand must contain 5 cards!")
        if list(dict.fromkeys(handStrList)) != handStrList:
            raise Exception("Hand cannot contain duplicate cards!")

        try:
            hand_of_cards = []
            for cardStr in handStrList:
                hand_of_cards.append(Card(cardStr))
            self.hand_value = self.calc_hand_value(hand_of_cards)
        except:
            raise Exception("One or more cards invalid!")

        self._logger.debug("Poker Hand: " + self.handStr + ": " + self.hand_value.name)
    
    def get_value(self):
        return self.hand_value

    # Return a PokerHandValue for this hand
    def calc_hand_value(self, hand_of_cards):
        # Sort by value, highest first (ace high)
        hand_of_cards = sorted(hand_of_cards, key=lambda card: card.get_value(), reverse=True)

        highest_card = None
        first_seen_suit = None
        all_same_suit = True
        previous_card = None
        num_in_sequence = 1
        all_in_sequence = True
        cardCounter = {}
        for card in hand_of_cards:
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
            return PokerHandValue.Pair
        elif matching_card_count == [2, 2, 1]:
            return PokerHandValue.TwoPairs
        elif matching_card_count == [3, 1, 1]:
            return PokerHandValue.ThreeOfAKind
        elif matching_card_count == [4, 1]:
            return PokerHandValue.FourOfAKind
        elif matching_card_count == [3, 2]:
            return PokerHandValue.FullHouse
        elif matching_card_count == [1, 1, 1, 1, 1]:
            if all_same_suit:
                if all_in_sequence:
                    if highest_card == CardValue.Ace:
                        return PokerHandValue.RoyalFlush
                    else:
                        return PokerHandValue.StraightFlush
                else:
                    return PokerHandValue.Flush
            elif all_in_sequence:
                return PokerHandValue.Straight
            else:
                return PokerHandValue.HighCard
        else:
            raise Exception("Unexpected card combination!")

    # Compare this hand with another hand
    # First compare hand value (e.g. pair beats high card)
    # If they match, apply more complicated draw rules
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if self.get_value() != other.get_value():
                # Compare by hand value
                # PokerHandValue ordered lower to higher
                # but sort better hands first, confusingly less than
                # TODO reorder PokerHandValue?
                return self.get_value() > other.get_value()
            else:
                # TODO Hands are the same, evaluate draw rules
                return NotImplemented
        return NotImplemented
