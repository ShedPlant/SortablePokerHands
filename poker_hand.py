import logging
import collections
from card             import Card
from card_value       import CardValue
from poker_hand_value import PokerHandValue

# A hand of five cards whose value can be compared against another hand
# according to Poker rules
# https://en.wikipedia.org/wiki/List_of_poker_hands
class PokerHand(object):
    def __repr__(self): return self.hand_as_string

    def __init__(self, hand_as_string):
        self._logger = logging.getLogger(__name__)

        # A string representation, never changed after initialisation
        # e.g. "5C 9D KH 9C 3S"
        self.hand_as_string = hand_as_string

        # Input validation
        hand_as_list = hand_as_string.split()
        # ["5C", "9D", "KH", "9C", "3S"]
        if len(hand_as_list) != 5:
            raise Exception("Hand must contain 5 cards!")
        if list(dict.fromkeys(hand_as_list)) != hand_as_list:
            # CodeWarrior tests contain at least one duplicate card in a hand
            # which I believe is a bug in the *test* not this class,
            # but I can't change the test.
            # (unless you were playing with multiple packs?)
            #
            # raise Exception("Hand cannot contain duplicate cards!")
            pass

        try:
            # Convert string to list of Card objects
            hand_as_list_of_card = []
            for card_as_string in hand_as_list:
                hand_as_list_of_card.append(Card(card_as_string))
        except Exception as e:
            # TODO use more specific, perhaps custom, exceptions?
            self._logger.warning("Poker Hand: \"" + self.hand_as_string + "\" failed!\n" + str(e))
            raise e

        # Just look at card values, ignore suits
        # Want it sorted:
        # Groups with more cards take precedence.
        # If groups of equal size, highest card takes precedence.
        # Achieve this by two sorts in reverse order.
        self.hands_sorted_by_group_value = collections.Counter(getattr(card, 'value') for card in hand_as_list_of_card)
        #self._logger.debug(self.hands_sorted_by_group_value)
        #Counter({<CardValue.Nine: '9'>: 2, <CardValue.Five: '5'>: 1, <CardValue.King: 'K'>: 1, <CardValue.Three: '3'>: 1})

        self.hands_sorted_by_group_value = dict(sorted(self.hands_sorted_by_group_value.items(), key=lambda item: item[0]))
        #self._logger.debug(self.hands_sorted_by_group_value)
        # {<CardValue.King: 'K'>: 1, <CardValue.Nine: '9'>: 2, <CardValue.Five: '5'>: 1, <CardValue.Three: '3'>: 1}

        self.hands_sorted_by_group_value = dict(sorted(self.hands_sorted_by_group_value.items(), key=lambda item: item[1], reverse=True))
        #self._logger.debug(self.hands_sorted_by_group_value)
        # {<CardValue.Nine: '9'>: 2, <CardValue.King: 'K'>: 1, <CardValue.Five: '5'>: 1, <CardValue.Three: '3'>: 1}

        group_counts = list(self.hands_sorted_by_group_value.values())
        first_group_count = group_counts[0]
        second_group_count = group_counts[1]
        if first_group_count == 1:
            if (CardValue.Ace   in self.hands_sorted_by_group_value and
                CardValue.Two   in self.hands_sorted_by_group_value and
                CardValue.Three in self.hands_sorted_by_group_value and
                CardValue.Four  in self.hands_sorted_by_group_value and
                CardValue.Five  in self.hands_sorted_by_group_value):
                # Move Ace to Ace Low
                # This hand combination is the *only* time it's ever used
                self.hands_sorted_by_group_value[CardValue.AceLow] = self.hands_sorted_by_group_value.pop(CardValue.Ace)
                
            previous_val = None
            straight = True
            for current_val in self.hands_sorted_by_group_value:
                if previous_val:
                    if previous_val - current_val != -1:
                        straight = False
                        break

                previous_val = current_val

            unique_suits = set(getattr(card, 'suit') for card in hand_as_list_of_card)
            if len(unique_suits) == 1:
                if straight:
                    # Simpler to treat Royal Flush as a Straight Flush,
                    # rather than its own type of hand.
                    self.hand_value = PokerHandValue.StraightFlush
                else:
                    self.hand_value = PokerHandValue.Flush
            elif straight:
                self.hand_value = PokerHandValue.Straight
            else:
                self.hand_value = PokerHandValue.HighCard
        elif first_group_count == 2:
            if second_group_count == 1:
                self.hand_value = PokerHandValue.Pair
            elif second_group_count == 2:
                self.hand_value = PokerHandValue.TwoPairs
        elif first_group_count == 3:
            if second_group_count == 1:
                self.hand_value = PokerHandValue.ThreeOfAKind
            elif second_group_count == 2:
                self.hand_value = PokerHandValue.FullHouse
        elif first_group_count == 4:
            self.hand_value = PokerHandValue.FourOfAKind
        else:
            raise Exception("Internal error while processing: " + self.hand_as_string)

        # Save the (possibly manipulated due to low ace rule) list of card values, for comparison
        self.hand_sorted_for_draw_comparison = list(self.hands_sorted_by_group_value.keys())



    # Compare this hand with another hand
    # First compare hand PokerHandValue, if they do not match there is a winner.
    #
    # If the two hands have same PokerHandValue,
    # Groups with more cards take precedence.
    # If groups of equal size, highest card takes precedence.
    #
    # @param self  = this object
    # @param other = another PokerHand object
    # @return True if self wins, False if other wins or same
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if self.hand_value != other.hand_value:
                # Hands differ
                return self.hand_value < other.hand_value
            else:
                # Hands are the same, compare pre-sorted lists
                return self.hand_sorted_for_draw_comparison < other.hand_sorted_for_draw_comparison
        return NotImplemented
