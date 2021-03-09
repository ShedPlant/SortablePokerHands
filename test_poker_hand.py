import unittest
import logging
from random import shuffle

from poker_hand import PokerHand
from poker_hand_value import PokerHandValue

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
        "HighCardLower": "TC 4H 7D KC 2S",
        "HighCardHigher": "TC 4H 7D AC 2S",
    }
}

@unittest.skip("Disable for now")
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

@unittest.skip("Disable for now")
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

class TestPokerHandSorting(unittest.TestCase):
    # Simple case
    def test_pair_beats_high_card(self):
        manually_sorted_hands = []
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.Pair.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.HighCard.name]))

        automatically_sorted_hands = manually_sorted_hands.copy()
        # Shuffle before sorting
        automatically_sorted_hands.reverse()
        # Back to original now
        automatically_sorted_hands.sort()
        self.assertEqual(manually_sorted_hands, automatically_sorted_hands)

    #@unittest.skip("Disable for now")
    def test_sort_all_hands(self):
        manually_sorted_hands = []
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.RoyalFlush.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.StraightFlush.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.FourOfAKind.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.FullHouse.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.Flush.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.Straight.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.ThreeOfAKind.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.TwoPairs.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.Pair.name]))
        manually_sorted_hands.append(PokerHand(test_hands["valid"][PokerHandValue.HighCard.name]))

        automatically_sorted_hands = manually_sorted_hands.copy()
        shuffle(automatically_sorted_hands)
        automatically_sorted_hands.sort()
        self.assertEqual(manually_sorted_hands, automatically_sorted_hands)

    #@unittest.skip("Disable for now")
    def test_draw_high_card(self):
        manually_sorted_hands = []
        manually_sorted_hands.append(PokerHand(test_hands["draws"]["HighCardHigher"]))
        manually_sorted_hands.append(PokerHand(test_hands["draws"]["HighCardLower"]))

        automatically_sorted_hands = manually_sorted_hands.copy()
        # Shuffle before sorting
        automatically_sorted_hands.reverse()
        # Back to original now
        automatically_sorted_hands.sort()

        self.assertEqual(manually_sorted_hands, automatically_sorted_hands)

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