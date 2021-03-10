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

        self.hands_sorted_by_group_value = dict(sorted(self.hands_sorted_by_group_value.items(), key=lambda item: item[0], reverse=True))
        #self._logger.debug(self.hands_sorted_by_group_value)
        # {<CardValue.King: 'K'>: 1, <CardValue.Nine: '9'>: 2, <CardValue.Five: '5'>: 1, <CardValue.Three: '3'>: 1}

        self.hands_sorted_by_group_value = dict(sorted(self.hands_sorted_by_group_value.items(), key=lambda item: item[1], reverse=True))
        #self._logger.debug(self.hands_sorted_by_group_value)
        # {<CardValue.Nine: '9'>: 2, <CardValue.King: 'K'>: 1, <CardValue.Five: '5'>: 1, <CardValue.Three: '3'>: 1}

        # Get a list of the number of matching cards (regardless of their face value)
        # Then can return appropriate PokerHandValue
        group_count = list(self.hands_sorted_by_group_value.values())
        #self._logger.debug(group_count)
        if group_count == [2, 1, 1, 1]:
            self.hand_value = PokerHandValue.Pair
        elif group_count == [2, 2, 1]:
            self.hand_value = PokerHandValue.TwoPairs
        elif group_count == [3, 1, 1]:
            self.hand_value = PokerHandValue.ThreeOfAKind
        elif group_count == [4, 1]:
            self.hand_value = PokerHandValue.FourOfAKind
        elif group_count == [3, 2]:
            self.hand_value = PokerHandValue.FullHouse
        elif group_count == [1, 1, 1, 1, 1]:

            if (CardValue.Ace   in self.hands_sorted_by_group_value and
                CardValue.Two   in self.hands_sorted_by_group_value and
                CardValue.Three in self.hands_sorted_by_group_value and
                CardValue.Four  in self.hands_sorted_by_group_value and
                CardValue.Five  in self.hands_sorted_by_group_value):
                # Move Ace to Ace Low
                # This hand combination is the *only* time it's ever used
                self.hands_sorted_by_group_value[CardValue.AceLow] = self.hands_sorted_by_group_value.pop(CardValue.Ace)
                
            previous_val = None
            num_in_sequence = 1
            for current_val in self.hands_sorted_by_group_value:
                if previous_val:
                    if previous_val - current_val == 1:
                        num_in_sequence = num_in_sequence + 1

                previous_val = current_val

            unique_suits = set(getattr(card, 'suit') for card in hand_as_list_of_card)
            if len(unique_suits) == 1:
                if num_in_sequence == len(self.hands_sorted_by_group_value):
                    # Royal Flush is not considered a separate Poker Hand Value
                    self.hand_value = PokerHandValue.StraightFlush
                else:
                    self.hand_value = PokerHandValue.Flush
            elif num_in_sequence == len(self.hands_sorted_by_group_value):
                self.hand_value = PokerHandValue.Straight
            else:
                self.hand_value = PokerHandValue.HighCard
        else:
            raise Exception("Unexpected group count!\n" + str(group_count))


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
                # Compare by hand value
                # PokerHandValue ordered lower to higher
                # but sort better hands first, confusingly less than
                # TODO reorder PokerHandValue?
                return self.hand_value > other.hand_value
            else:
                # Hands are the same, evaluate draw rules
                # https://www.journaldev.com/37089/how-to-compare-two-lists-in-python
                for mine, theirs in zip(self.hands_sorted_by_group_value, other.hands_sorted_by_group_value):
                    if mine != theirs:
                        return mine > theirs

                # Same value of all five cards
                # Stable sorting
                return False
        return NotImplemented
