import unittest
import logging
from random import shuffle

from poker_hand import PokerHand
from poker_hand_value import PokerHandValue

# TODO some of this could be moved to more specific test classes e.g. draws, invalid
test_hands = {
    "valid": {
        "HighCard": "TC 4H 7D KC 2S",
        "Pair": "KC KH 7D 2C 5S",
        "TwoPairs": "KC KH 7D 7C 5S",
        "ThreeOfAKind": "KC KH KD 7C 5S",
        "Straight": "3C 4H 5D 6C 7S",
        "StraightLowAce": "3C 4H 5D 2C AS",
        "Flush": "2C 8C 9C QC KC",
        "FullHouse": "7C KC KH 7S KS",
        "FourOfAKind": "KS 6S 6D 6H 6C",
        "StraightFlush": "5S 6S 2S 3S 4S",
        "RoyalFlush": "KS AS TS QS JS"
    },
    "invalid": {
        "Empty": "",
        "TooFewCards": "KS AS TS QS",
        "TooManyCards": "KS AS TS QS JS 1S",
        "InvalidValue": "KS AS TS QS XS",
        "InvalidSuit": "KS AS TS QS JX",
        "Duplicates": "KS AS TS QS QS"
    },
    "draws": {
        "HighCard": {
            "Lower":  "TC 4H 7D KC 2S",
            "Middle": "JC 4H 7D KC 2S",
            "Higher": "TC 4H 7D AC 2S"
        },
        "Pair": {
            "Lower":  "KC 8C 8H 7D 5S",
            "Middle": "5S 8C 8H 7D AC",
            "Higher": "KC 7D KH 2C 5S"
        },
        "TwoPairs": {
            "Lower":  "QC QH 6D 6C 5S",
            "Middle": "QC QH 7D 7C 5S",
            "Higher": "KC KH 7D 7C 5S"
        },
        "ThreeOfAKind": {
            "Lower":  "JC JH JD 7C 5S",
            "Middle": "QC QH QD 7C 5S",
            "Higher": "KC KH KD 7C 5S"
        },
        "Straight": {
            "Lower":  "3C 4H 5D 6C 7S",
            "Middle": "4H 5D 6C 7S 8C",
            "Higher": "5D 6C 7S 8C 9H"
        },
        "Flush": {
            "Lower":  "2C 8C 9C QC TC",
            "Middle": "2C 8C 9C QC KC",
            "Higher": "2C 8C 9C QC AC",
            "Spades": "2S 8S 9S QS AS",
            "Hearts": "2H 8H 9H QH AH",
            "Diamonds": "2D 8D 9D QD AD",
            "Clubs":  "2C 8C 9C QC AC"
        },
        "FullHouse": {
            "Lower":  "5C QC QH 5S QS",
            "Middle": "5C KC KH 5S KS",
            "Higher": "7C KC KH 7S KS"
        },
        "FourOfAKind": {
            "Lower":  "QS 5S 5D 5H 5C",
            "Middle": "KS 5S 5D 5H 5C",
            "Higher": "KS 6S 6D 6H 6C"
        },
        "StraightFlush": {
            "Lower":  "5S 6S 2S 3S 4S",
            "Middle": "5S 6S 3S 4S 7S",
            "Higher": "5S 8S 6S 4S 7S"
        }
    }
}

#@unittest.skip("Disable for now")
class TestPokerHandErrorHandling(unittest.TestCase):
    # TODO use more specific, perhaps custom, exceptions?

    def test_no_cards(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands["invalid"]["Empty"])

    def test_too_few_cards(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands["invalid"]["TooFewCards"])

    def test_too_many_cards(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands["invalid"]["TooManyCards"])

    def test_invalid_value(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands["invalid"]["InvalidValue"])

    def test_invalid_suit(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands["invalid"]["InvalidSuit"])

    def test_no_duplicates_allowed(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands["invalid"]["Duplicates"])

#@unittest.skip("Disable for now")
class TestPokerHandValue(unittest.TestCase):
    def assertHandValuedCorrectly(self, poker_hand_value):
        hand_string = test_hands["valid"][poker_hand_value.name]
        self.assertEqual(
            PokerHand(hand_string).get_value(),
            poker_hand_value
        )

    def test_royal_flush(self):
        self.assertHandValuedCorrectly(PokerHandValue.RoyalFlush)

    def test_straight_flush(self):
        self.assertHandValuedCorrectly(PokerHandValue.StraightFlush)

    def test_four_of_a_kind(self):
        self.assertHandValuedCorrectly(PokerHandValue.FourOfAKind)

    def test_full_house(self):
        self.assertHandValuedCorrectly(PokerHandValue.FullHouse)

    def test_flush(self):
        self.assertHandValuedCorrectly(PokerHandValue.Flush)

    def test_straight(self):
        self.assertHandValuedCorrectly(PokerHandValue.Straight)

    def test_straight_low_ace(self):
        hand_string = test_hands["valid"]["StraightLowAce"]
        self.assertEqual(
            PokerHand(hand_string).get_value(),
            PokerHandValue.Straight
        )

    def test_three_of_a_kind(self):
        self.assertHandValuedCorrectly(PokerHandValue.ThreeOfAKind)

    def test_two_pairs(self):
        self.assertHandValuedCorrectly(PokerHandValue.TwoPairs)

    def test_pair(self):
        self.assertHandValuedCorrectly(PokerHandValue.Pair)

    def test_high_card(self):
        self.assertHandValuedCorrectly(PokerHandValue.HighCard)

#@unittest.skip("Disable for now")
class TestPokerHandSorting(unittest.TestCase):
    def shuffleAndConfirmHandsSorted(self, list_of_hand_strings):
        manually_sorted_hands = []
        for hand_string in list_of_hand_strings:
            manually_sorted_hands.append(PokerHand(hand_string))
        automatically_sorted_hands = manually_sorted_hands.copy()

        number_of_hands = len(automatically_sorted_hands)
        if number_of_hands == 2:
            automatically_sorted_hands.reverse()
        else:
            shuffle(automatically_sorted_hands)

        automatically_sorted_hands.sort()
        self.assertEqual(manually_sorted_hands, automatically_sorted_hands)

    # Simplest comparison case
    #@unittest.skip("Might be useful for debugging but implicit in test_all_hand_types_sorted")
    #@unittest.skip("Disable for now")
    def test_pair_beats_high_card(self):
        self.shuffleAndConfirmHandsSorted([
            test_hands["valid"][PokerHandValue.Pair.name],
            test_hands["valid"][PokerHandValue.HighCard.name]
        ] )

    #@unittest.skip("Disable for now")
    def test_all_hand_types_sorted(self):
        self.shuffleAndConfirmHandsSorted([
            test_hands["valid"][PokerHandValue.RoyalFlush.name],
            test_hands["valid"][PokerHandValue.StraightFlush.name],
            test_hands["valid"][PokerHandValue.FourOfAKind.name],
            test_hands["valid"][PokerHandValue.FullHouse.name],
            test_hands["valid"][PokerHandValue.Flush.name],
            test_hands["valid"][PokerHandValue.Straight.name],
            test_hands["valid"][PokerHandValue.ThreeOfAKind.name],
            test_hands["valid"][PokerHandValue.TwoPairs.name],
            test_hands["valid"][PokerHandValue.Pair.name],
            test_hands["valid"][PokerHandValue.HighCard.name]
        ] )

    def shuffleAndConfirmDrawSorted(self,poker_hand_value):
        self.shuffleAndConfirmHandsSorted([
            test_hands["draws"][poker_hand_value.name]["Higher"],
            test_hands["draws"][poker_hand_value.name]["Middle"],
            test_hands["draws"][poker_hand_value.name]["Lower"]
        ] )

    def test_draw_high_card(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.HighCard)

    def test_draw_pair(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.Pair)

    #@unittest.skip("Disable for now")
    def test_draw_two_pairs(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.TwoPairs)

    #@unittest.skip("Disable for now")
    def test_draw_three_of_a_kind(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.ThreeOfAKind)

    #@unittest.skip("Disable for now")
    def test_draw_straight(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.Straight)

    #@unittest.skip("Disable for now")
    def test_draw_flush(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.Flush)

    @unittest.skip("Disable for now")
    @unittest.expectedFailure
    def test_draw_same(self):
        self.shuffleAndConfirmHandsSorted([
            test_hands["draws"][PokerHandValue.Flush.name]["Spades"],
            test_hands["draws"][PokerHandValue.Flush.name]["Hearts"],
            test_hands["draws"][PokerHandValue.Flush.name]["Diamonds"],
            test_hands["draws"][PokerHandValue.Flush.name]["Clubs"]
        ] )

    @unittest.skip("Disable for now")
    def test_draw_full_house(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.FullHouse)

    #@unittest.skip("Disable for now")
    def test_draw_four_of_a_kind(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.FourOfAKind)

    #@unittest.skip("Disable for now")
    def test_draw_straight_flush(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.StraightFlush)

    # By definition, two royal flush hands have same value
    # Undefined sorting


    # TODO sorting tests to resolve complex draws
    # (e.g. two hands have two pair with same higher card)
    
    # TODO Kickers

if __name__ == "__main__":
    _logger = logging.getLogger(__name__)
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)-15s - %(levelname)s - %(message)s'
    )
    _logger.info("Sortable Poker Hands")
    _logger.info("Author: Ed Plant")
    unittest.main()