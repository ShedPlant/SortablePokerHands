import unittest
import logging
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
            PokerHand(test_hands.get("invalid.TooFewCards"))

    def test_too_many_cards(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands.get("invalid.TooManyCards"))

    def test_invalid_value(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands.get("invalid.InvalidValue"))

    def test_invalid_suit(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands.get("invalid.InvalidSuit"))

    def test_no_duplicates_allowed(self):
        with self.assertRaises(Exception):
            PokerHand(test_hands.get("invalid.Duplicates"))

class TestPokerHandValue(unittest.TestCase):
    def assertHandValuedCorrectly(self, poker_hand_value):
        #hand_string = test_hands("valid", {}).get(poker_hand_value.name)
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

# TODO sorting tests
# TODO sorting tests to resolve draws (e.g. higher pair)
class TestPokerHandSorting(unittest.TestCase):
    def test_pair_beats_high_card(self):
        pass

if __name__ == "__main__":
    _logger = logging.getLogger(__name__)
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)-15s - %(levelname)s - %(message)s'
    )
    _logger.info("Sortable Poker Hands")
    _logger.info("Author: Ed Plant")
    unittest.main()