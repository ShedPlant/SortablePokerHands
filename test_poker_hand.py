import unittest
from poker_hand import PokerHand
from poker_hand_value import PokerHandValue

royal_flush = "KS AS TS QS JS"
straight_flush = "5S 6S 2S 3S 4S"
four_of_a_kind = "KS 6S 6D 6H 6C"
full_house = "7C KC KH 7S KH"
flush = "2C 8C 9C QC KC"
straight = "3C 4H 5D 6C 7S"
three_of_a_kind = "KC KH KD 7C 5S"
two_pairs = "KC KH 7D 7C 5S"
pair = "KC KH 7D 2C 5S"
high_card = "10C 4H 7D KC 2S"

class TestPokerHandValidation(unittest.TestCase):
    def test_simple_hand_creation(self):
        self.assertEqual(repr(PokerHand(royal_flush)),royal_flush)

    # TODO use more specific, perhaps custom, exceptions

    def test_no_cards(self):
        with self.assertRaises(Exception):
            PokerHand("")

    def test_too_few_cards(self):
        with self.assertRaises(Exception):
            PokerHand("KS AS TS QS")

    def test_too_many_cards(self):
        with self.assertRaises(Exception):
            PokerHand("KS AS TS QS JS 1S")

    def test_invalid_value(self):
        with self.assertRaises(Exception):
            PokerHand("KS AS TS QS XS")

    def test_invalid_suit(self):
        with self.assertRaises(Exception):
            PokerHand("KS AS TS QS JX")

    def test_no_duplicates_allowed(self):
        with self.assertRaises(Exception):
            PokerHand("KS AS TS QS QS")

class TestPokerHandValue(unittest.TestCase):
    # TODO All fail
    def test_royal_flush(self):
        self.assertEqual(
            PokerHand(royal_flush).get_value(),
            PokerHandValue.RoyalFlush
        )

    def test_straight_flush(self):
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
        )

# TODO sorting tests

if __name__ == "__main__":
    unittest.main()