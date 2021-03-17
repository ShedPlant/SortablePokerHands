import logging
from collections import Counter
from card import Card
from card_value import CardValue
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

        # CodeWarrior tests contain at least one duplicate card in a hand
        # which I believe is a bug in the *test* not this class,
        # but I can't change the test.
        # (unless you were playing with multiple packs?)

        try:
            # Convert string to list of Card objects
            cards_in_hand = []
            for card_as_string in hand_as_string.split():
                cards_in_hand.append(Card(card_as_string))

            if len(cards_in_hand) != 5:
                raise Exception("Hand must contain 5 cards!")
        except Exception as e:
            # TODO use more specific, perhaps custom, exceptions?
            self._logger.warning(
                "Poker Hand: \"" + self.hand_as_string +
                "\" failed!\n" + str(e))
            raise e

        # Poker hands ties are resolved by:
        # 1st: Larger groups over smaller (e.g. ThreeOfaKind beats Pair)
        # 2nd: Larger value over smaller  (e.g. kicker Ace beats kicker King)
        #
        # To achieve two sorts, do in reverse:
        # sort by value *first*
        # then use Counter to sort by group sizes
        cards_in_hand.sort(reverse=True)

        # A counter of CardValue object counts
        c = Counter(getattr(card, 'value') for card in cards_in_hand)

        # A list of (score, count) lists, sorted by biggest groups
        grouped_sorted_vals = c.most_common()

        # A list of CardValue objects
        # with duplicates removed, for later tiebreaking
        # e.g. if hand was four of a kind of Jack,
        # only add one Jack for the group.
        # It will only be compared to another hand with four of a kind
        grouped_sorted_unq_vals = list(dict(grouped_sorted_vals))

        first_group_size = grouped_sorted_vals[0][1]
        second_group_size = grouped_sorted_vals[1][1]
        if first_group_size == 1:
            # We already know there are 5 unique cards in descending order.
            # So, if first is Ace and second is Five,
            # it follows that the rest are Four, Three, Two.
            if (grouped_sorted_unq_vals[0] == CardValue.ACE and
                    grouped_sorted_unq_vals[1] == CardValue.FIVE):
                # Move Ace from beginning to Ace Low at end
                # This hand combination is the *only* time it's ever used
                grouped_sorted_unq_vals.pop(0)
                grouped_sorted_unq_vals.append(CardValue.ACE_LOW)

            previous_val = None
            straight = True
            for current_val in grouped_sorted_unq_vals:
                if previous_val:
                    if previous_val - current_val != 1:
                        straight = False
                        break
                previous_val = current_val

            unique_suits = set(getattr(card, 'suit') for card in cards_in_hand)
            if len(unique_suits) == 1:
                if straight:
                    # Simpler to treat Royal Flush as a Straight Flush,
                    # rather than its own type of hand.
                    self.hand_value = PokerHandValue.STRAIGHT_FLUSH
                else:
                    self.hand_value = PokerHandValue.FLUSH
            elif straight:
                self.hand_value = PokerHandValue.STRAIGHT
            else:
                self.hand_value = PokerHandValue.HIGH_CARD
        elif first_group_size == 2:
            if second_group_size == 1:
                self.hand_value = PokerHandValue.PAIR
            elif second_group_size == 2:
                self.hand_value = PokerHandValue.TWO_PAIRS
        elif first_group_size == 3:
            if second_group_size == 1:
                self.hand_value = PokerHandValue.THREE_OF_A_KIND
            elif second_group_size == 2:
                self.hand_value = PokerHandValue.FULL_HOUSE
        elif first_group_size == 4:
            self.hand_value = PokerHandValue.FOUR_OF_A_KIND
        else:
            raise Exception(
                "Internal error while processing: " + self.hand_as_string)

        """
        Final Hand Score is used to compare hands
        and resolve ties as quickly efficiently as possible.
        It is a tuple (immutable list) of:
        - a PokerHandValue object's raw integer score
        - the 1st biggest group's raw integer score
        - the 2nd biggest group's raw integer score
        - the 3rd biggest group's raw integer score (if applicable)
        - the 4th biggest group's raw integer score (if applicable)
        - the 5th biggest group's raw integer score (if applicable)

        e.g. for "5C 9D KH 9C 3S"
        |-------|-------------|---------------------|---------|
        | index | description |         from object | raw int |
        |-------|-------------|---------------------|---------|
        |     0 |  Hand Value | PokerHandValue.Pair |       2 |
        |     1 |   1st Group |      CardValue.Nine |       9 |
        |     2 |   2nd Group |      CardValue.King |      13 |
        |     3 |   3rd Group |      CardValue.Five |       5 |
        |     4 |   4th Group |     CardValue.Three |       3 |
        |     5 |   5th Group |                     |         |
        |-------|-------------|---------------------|---------|
        """
        self.score = [self.hand_value.value]
        self.score.extend(
            getattr(cv, 'score') for cv in grouped_sorted_unq_vals
        )
        # https://stackoverflow.com/questions/35004882/make-a-list-of-ints-hashable-in-python
        # Tuple is hashable for speed
        self.score = tuple(self.score)

    # Compare this hand score with another hand score
    # @param self  = this object
    # @param other = another PokerHand object
    #
    # @return True if self wins, False if other wins or same
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            # Counter intuitive but 'less' means 'sort first'
            # Sort higher ranked cards first
            return self.score > other.score
        return NotImplemented

    # Compare this hand score with another hand score
    # @param self  = this object
    # @param other = another PokerHand object
    #
    # @return True if scores equal
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self.score == other.score
        return NotImplemented
