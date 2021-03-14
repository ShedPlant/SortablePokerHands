import logging
from collections      import Counter
from card             import Card
from card_value       import CardValue, VALID_VALUES
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
            unsorted_cards = []
            for card_as_string in hand_as_list:
                unsorted_cards.append(Card(card_as_string))
        except Exception as e:
            # TODO use more specific, perhaps custom, exceptions?
            self._logger.warning("Poker Hand: \"" + self.hand_as_string + "\" failed!\n" + str(e))
            raise e

        # Poker hands ties are resolved by:
        # 1st: Larger groups over smaller (e.g. ThreeOfaKind beats Pair)
        # 2nd: Larger value over smaller  (e.g. kicker Ace beats kicker King)
        #
        # To achieve two sorts, do in reverse:
        # sort by value *first*
        # then use Counter to sort by group sizes
        ungrouped_sorted_vals = sorted(getattr(card, 'value') for card in unsorted_cards)
        c = Counter(getattr(card_value, 'value') for card_value in ungrouped_sorted_vals)
        grouped_sorted_vals = c.most_common()
        grouped_sorted_unq_vals = list(dict(grouped_sorted_vals))

        first_group_size = grouped_sorted_vals[0][1]
        second_group_size = grouped_sorted_vals[1][1]
        if first_group_size == 1:
            # We already know there are 5 unique cards in descending order.
            # So, if first is Ace and second is Five,
            # it follows that the rest are Four, Three, Two.
            if (grouped_sorted_unq_vals[0] == VALID_VALUES["A"]["value"] and
                grouped_sorted_unq_vals[1] == VALID_VALUES["5"]["value"]):
                # Move Ace from beginning to Ace Low at end
                # This hand combination is the *only* time it's ever used
                grouped_sorted_unq_vals.pop(0)
                grouped_sorted_unq_vals.append(CardValue("a").value)
                
            previous_val = None
            straight = True
            for current_val in grouped_sorted_unq_vals:
                if previous_val:
                    if previous_val - current_val != 1:
                        straight = False
                        break
                previous_val = current_val

            unique_suits = set(getattr(card, 'suit') for card in unsorted_cards)
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
        elif first_group_size == 2:
            if second_group_size == 1:
                self.hand_value = PokerHandValue.Pair
            elif second_group_size == 2:
                self.hand_value = PokerHandValue.TwoPairs
        elif first_group_size == 3:
            if second_group_size == 1:
                self.hand_value = PokerHandValue.ThreeOfAKind
            elif second_group_size == 2:
                self.hand_value = PokerHandValue.FullHouse
        elif first_group_size == 4:
            self.hand_value = PokerHandValue.FourOfAKind
        else:
            raise Exception("Internal error while processing: " + self.hand_as_string)

        """
        Final Hand Score is a tuple (immutable list) of between 3 and 6 raw integers
        to compare hands and resolve ties, as efficiently as possible.
        e.g. for "5C 9D KH 9C 3S" (a pair of nines)
        |-------|-------------|----------------|---------------------|-----------|
        | index |        desc | always present |                from | raw value |
        |-------|-------------|----------------|---------------------|-----------|
        |     0 |  Hand Value |           True | PokerHandValue.Pair |         2 |
        |     1 |   1st Group |           True |      CardValue.Nine |         9 |
        |     2 |   2nd Group |           True |      CardValue.King |        13 |
        |     3 |   3rd Group |          False |      CardValue.Five |         5 |
        |     4 |   4th Group |          False |     CardValue.Three |         3 |
        |     5 |   5th Group |          False |                     |           |
        |-------|-------------|----------------|---------------------|-----------|
        """
        self.score = [ self.hand_value.value ]
        self.score.extend(grouped_sorted_unq_vals)
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
