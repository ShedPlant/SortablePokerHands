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
        self.hand_as_string = hand_as_string
        # A list of Card objects
        self.hand_of_cards = []

        # PokerHandValue
        self.hand_value = None

        # Reordered hand_of_cards for tie-breaking situation
        self.card_counter = None
        self.tiebreaker = None

        # Input validation
        hand_as_list = hand_as_string.split()
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
            for card_as_string in hand_as_list:
                self.hand_of_cards.append(Card(card_as_string))

            # https://stackoverflow.com/a/40789844
            self.card_counter = collections.Counter(getattr(card, 'value') for card in self.hand_of_cards)

            # Get the hand value
            self.hand_value = self.calc_hand_value(self.hand_of_cards)
            #self._logger.debug("Poker Hand: \"" + self.hand_as_string + "\": " + self.hand_value.name)
        except Exception as e:
            # TODO use more specific, perhaps custom, exceptions?
            self._logger.warning("Poker Hand: \"" + self.hand_as_string + "\" failed!\n" + str(e))
            raise e

    
    def get_value(self):
        return self.hand_value


    def get_tiebreaker(self):
        if not self.tiebreaker:
            # Don't calculate on object creation, for speed
            # since not always needed
            self.tiebreaker = self.calc_tiebreaker(self.hand_of_cards)

        return self.tiebreaker


    # Calculate a hand value (e.g. pair or full house)
    #
    # @param hand_of_cards = a list of 5 Card objects
    # @return a PokerHandValue for hand_of_cards
    def calc_hand_value(self, hand_of_cards):
        # hand_of_cards is a local variable, this proc doesn't manipulate the object's hand.
        highest_card = None
        first_seen_suit = None
        all_same_suit = True
        previous_card = None
        num_in_sequence = 1
        all_in_sequence = True
        low_ace_adjusted = False

        # Sort by value, highest first (ace high), ignoring suit
        # TODO able to sort Card class natively by using its CardValue
        hand_of_cards = sorted(hand_of_cards, key=lambda card: card.get_value(), reverse=True)

        for card in hand_of_cards:
            if not highest_card:
                # List is already sorted, effectively just get the first card
                highest_card = card.get_value()
            if not first_seen_suit:
                first_seen_suit = card.get_suit()

            if card.get_suit() != first_seen_suit:
                all_same_suit = False

            if previous_card:
                if (previous_card.get_value() - card.get_value()) == 1:
                    # Cards are adjacent e.g. 3 and 4
                    num_in_sequence = num_in_sequence + 1

                # Special case, low ace adjacent to 2
                # So, can't use a simple boolean 'all_in_sequence', like done with suit
                if (not low_ace_adjusted and
                    card.get_value() == CardValue.Two and highest_card == CardValue.Ace):
                    num_in_sequence = num_in_sequence + 1
                    low_ace_adjusted = True

            previous_card = card

        if num_in_sequence != len(hand_of_cards):
            all_in_sequence = False

        # Get a list of the number of matching cards (regardless of their face value)
        # Then can return appropriate PokerHandValue
        matching_card_count = sorted(self.card_counter.values(), reverse=True)
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
                    if not low_ace_adjusted and highest_card == CardValue.Ace:
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


    # Calculate tie-breaker sorted list of Cards for comparing two hands with same PokerHandValue
    # Different PokerHandValue's have different rules about how to calculate draws
    #
    # @param hand_of_cards = a list of 5 Card objects
    #
    # @return tiebreaker = hand_of_cards re-ordered for easier comparison against another tiebreaker hand
    # e.g. for following input list of Card objects
    #      ["8C", "5S", "7D", "2C", "8H"]
    # e.g. put the pair of 8s first, then kickers in descending order
    #      ["8C", "8H", "7D", "5S", "2C"]
    def calc_tiebreaker(self, hand_of_cards):
        tiebreaker = []
        kickers = []

        if self.get_value().get_draw_sorting_type() in [
                "high_to_low",
                "high_to_low_ace_can_be_low"
            ]:
            # Sort by value, highest first (ace high), ignoring suit
            # TODO able to sort Card class natively by using its CardValue
            tiebreaker = sorted(hand_of_cards, key=lambda card: card.get_value(), reverse=True)

            if self.get_value().get_draw_sorting_type() == "high_to_low_ace_can_be_low":
                if tiebreaker[0].get_value() - tiebreaker[1].get_value() != 1:
                    low_ace_suit = tiebreaker[0].get_suit()
                    low_ace_string = "a" + low_ace_suit.value
                    tiebreaker.pop(0)
                    tiebreaker.append(Card(low_ace_string))
        elif self.get_value().get_draw_sorting_type() == "one_group_then_kickers":
            # TODO refactor so same code can handle one/two groups?
            most_common = self.card_counter.most_common(1)[0][0]
            # Insert group value, then kickers
            for card in hand_of_cards:
                if card.get_value() == most_common:
                    tiebreaker.append(card)
                    break
            for card in hand_of_cards:
                if card.get_value() != most_common:
                    kickers.append(card)
            kickers = sorted(kickers, key=lambda card: card.get_value(), reverse=True)
            tiebreaker = tiebreaker + kickers
        elif self.get_value().get_draw_sorting_type() == "two_groups_then_kickers":
            most_common = self.card_counter.most_common(2)
            first_group = most_common[0][0]
            second_group = most_common[1][0]

            # Collection returns pairs in order first seen,
            # but highest group should go first
            if first_group < second_group:
                first_group, second_group = second_group, first_group

            # Insert highest group, then second group, then kickers
            for card in hand_of_cards:
                if card.get_value() == first_group:
                    tiebreaker.append(card)
                    break
            for card in hand_of_cards:
                if card.get_value() == second_group:
                    tiebreaker.append(card)
                    break
            for card in hand_of_cards:
                if card.get_value() not in [first_group, second_group]:
                    kickers.append(card)
            kickers = sorted(kickers, key=lambda card: card.get_value(), reverse=True)
            tiebreaker = tiebreaker + kickers
        else:
            return NotImplemented

        return tiebreaker

    # Compare this hand with another hand
    # First compare hand PokerHandValue, if they match there is a winner.
    #
    # If the two hands have same PokerHandValue,
    # call get_tiebreaker (calc_tiebreaker) to reorder both hands
    # in such a way both hands can be compared one hand at a time
    # to find the winner.
    #
    # @param self  = this object
    # @param other = another PokerHand object
    # @return True if self wins, False if other wins or same
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            if self.get_value() != other.get_value():
                # Compare by hand value
                # PokerHandValue ordered lower to higher
                # but sort better hands first, confusingly less than
                # TODO reorder PokerHandValue?
                return self.get_value() > other.get_value()
            else:
                # Hands are the same, evaluate draw rules
                # https://www.journaldev.com/37089/how-to-compare-two-lists-in-python
                for mine, theirs in zip(self.get_tiebreaker(), other.get_tiebreaker()):
                    if mine.get_value() != theirs.get_value():
                        return mine.get_value() > theirs.get_value()

                # Same value of all five cards
                # Arbitrary sorting (possibly first seen?)
                return False
        return NotImplemented
