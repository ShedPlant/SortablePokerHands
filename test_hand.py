import unittest
from poker_hand import PokerHand

class TestPokerHandInputs(unittest.TestCase):
    def test_simple_hand_creation(self):
        royalFlushStr = "KS AS TS QS JS"
        royalFlushHand = PokerHand(royalFlushStr)
        self.assertEqual(repr(royalFlushHand),royalFlushStr)

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

#class TestPokerHandSorting(unittest.TestCase):


if __name__ == "__main__":
    unittest.main()