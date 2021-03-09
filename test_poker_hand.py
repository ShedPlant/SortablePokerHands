import unittest
from poker_hand import PokerHand
from poker_hand_value import PokerHandValue

testHands = {
    "HighCard": "10C 4H 7D KC 2S",
    "Pair": "KC KH 7D 2C 5S",
    "TwoPairs": "KC KH 7D 7C 5S",
    "ThreeOfAKind": "KC KH KD 7C 5S",
    "Straight": "3C 4H 5D 6C 7S",
    "Flush": "2C 8C 9C QC KC",
    "FullHouse": "7C KC KH 7S KH",
    "FourOfAKind": "KS 6S 6D 6H 6C",
    "StraightFlush": "5S 6S 2S 3S 4S",
    "RoyalFlush": "KS AS TS QS JS",

    "TooFewCards": "KS AS TS QS",
    "TooManyCards": "KS AS TS QS JS 1S",
    "InvalidValue": "KS AS TS QS XS",
    "InvalidSuit": "KS AS TS QS JX",
    "Duplicates": "KS AS TS QS QS"
}

class TestPokerHandValidation(unittest.TestCase):
    def test_simple_hand_creation(self):
        self.assertEqual(
            repr(PokerHand(testHands.get("RoyalFlush"))),
            testHands.get("RoyalFlush")
            )

    # TODO use more specific, perhaps custom, exceptions

    def test_no_cards(self):
        with self.assertRaises(Exception):
            PokerHand("")

    def test_too_few_cards(self):
        with self.assertRaises(Exception):
            PokerHand(testHands.get("TooFewCards"))

    def test_too_many_cards(self):
        with self.assertRaises(Exception):
            PokerHand(testHands.get("TooManyCards"))

    def test_invalid_value(self):
        with self.assertRaises(Exception):
            PokerHand(testHands.get("InvalidValue"))

    def test_invalid_suit(self):
        with self.assertRaises(Exception):
            PokerHand(testHands.get("InvalidSuit"))

    def test_no_duplicates_allowed(self):
        with self.assertRaises(Exception):
            PokerHand(testHands.get("Duplicates"))

"""class TestPokerHandValue(unittest.TestCase):
    # TODO All fail
    def test_royal_flush(self):
        self.assertEqual(
            PokerHand(royal_flush).get_value(),
            PokerHandValue.RoyalFlush
        ) """

"""     def test_straight_flush(self):
        self.assertEqual(
            PokerHand(straight_flush).get_value(),
            PokerHandValue.StraightFlush
        )

    def test_four_of_a_kind(self):
        self.assertEqual(
            PokerHand(four_of_a_kind).get_value(),
            PokerHandValue.FourOfAKind
        )

    def test_full_house(self):
        self.assertEqual(
            PokerHand(full_house).get_value(),
            PokerHandValue.FullHouse
        )

    def test_flush(self):
        self.assertEqual(
            PokerHand(flush).get_value(),
            PokerHandValue.Flush
        )

    def test_straight(self):
        self.assertEqual(
            PokerHand(straight).get_value(),
            PokerHandValue.Straight
        )

    def test_three_of_a_kind(self):
        self.assertEqual(
            PokerHand(three_of_a_kind).get_value(),
            PokerHandValue.ThreeOfAKind
        )

    def test_two_pairs(self):
        self.assertEqual(
            PokerHand(two_pairs).get_value(),
            PokerHandValue.TwoPairs
        )

    def test_pair(self):
        self.assertEqual(
            PokerHand(pair).get_value(),
            PokerHandValue.Pair
        )

    def test_high_card(self):
        self.assertEqual(
            PokerHand(high_card).get_value(),
            PokerHandValue.HighCard
        ) """

# TODO sorting tests
# TODO sorting tests to resolve draws (e.g. higher pair)

if __name__ == "__main__":
    unittest.main()