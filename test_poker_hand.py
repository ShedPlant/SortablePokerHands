import unittest
import logging
from random import shuffle

from poker_hand import PokerHand
from poker_hand_value import PokerHandValue
from dealer import Dealer

test_hands = {
    "HighCard": {
        "Lower":  "TC 4H 7D KC 2S",
        "Middle": "JC 4H 7D KC 2S",
        "Higher": "TC 4H 7D AC 2S"
    },
    "Pair": {
        "Lower":  "KC 8C 8H 7D 5S",
        "Middle": "5S 8C 8H 7D AC",
        "Higher": "5C 9D KH 9C 3S"
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
        "Lower":  "2C 3C AD 4H 5S",
        "Middle": "2D 6D 3D 4H 5S",
        "Higher": "5D 6C 7S 8C 9H"
    },
    "Flush": {
        "Lower":    "2C 8C 9C QC TC",
        "Middle":   "2C 8C 9C QC KC",
        "Higher":   "2C 8C 9C QC AC",
        "Spades":   "2S 8S 9S QS AS",
        "Hearts":   "2H 8H 9H QH AH",
        "Diamonds": "2D 8D 9D QD AD",
        "Clubs":    "3C 8C TC QC AC"
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
        "Lower":  "2C 3C AC 4C 5C",
        "Middle": "2D 6D 3D 4D 5D",
        "Higher": "KS AS TS QS JS"
    }
}

#@unittest.skip("Disable for now")
class TestPokerHandErrorHandling(unittest.TestCase):
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

    # Disabled exception to comply with codewars validation
    @unittest.expectedFailure
    def test_no_duplicates_allowed(self):
        with self.assertRaises(Exception):
            PokerHand("KS KS AS QS TS")

#@unittest.skip("Disable for now")
class TestPokerHandValue(unittest.TestCase):
    def assertHandValuedCorrectly(self, poker_hand_value):
        many_hands_list = []
        for order in ["Higher", "Middle", "Lower"]:
            many_hands_list.append(
                test_hands[poker_hand_value.name][order]
            )
        for hand_string in many_hands_list:
            self.assertEqual(
                PokerHand(hand_string).hand_value,
                poker_hand_value
            )

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
        if number_of_hands < 10:
            automatically_sorted_hands.reverse()
        else:
            shuffle(automatically_sorted_hands)

        automatically_sorted_hands.sort()
        self.assertEqual(manually_sorted_hands, automatically_sorted_hands)

    # Simple comparison case
    # although implicit in test_all_hands_types_sorted
    def test_pair_beats_high_card(self):
        # pylint: disable=maybe-no-member
        self.shuffleAndConfirmHandsSorted([
            test_hands[PokerHandValue.Pair.name]["Higher"],
            test_hands[PokerHandValue.HighCard.name]["Higher"]
        ] )

    def test_all_hand_types_sorted(self):
        # Aware that I could iterate over PokerHandValue members
        # but then would be vulnerable to bugs in that class
        # Here, the ordering is absolutely explicit.
        many_hands_list = []
        # pylint: disable=maybe-no-member
        for poker_hand_value in [
            PokerHandValue.StraightFlush.name,
            PokerHandValue.FourOfAKind.name,
            PokerHandValue.FullHouse.name,
            PokerHandValue.Flush.name,
            PokerHandValue.Straight.name,
            PokerHandValue.ThreeOfAKind.name,
            PokerHandValue.TwoPairs.name,
            PokerHandValue.Pair.name,
            PokerHandValue.HighCard.name,
        ]:
            for order in ["Higher", "Middle", "Lower"]:
                many_hands_list.append(
                    test_hands[poker_hand_value][order]
                )
            self.shuffleAndConfirmHandsSorted(many_hands_list)

    def shuffleAndConfirmDrawSorted(self,poker_hand_value):
        self.shuffleAndConfirmHandsSorted([
            test_hands[poker_hand_value.name]["Higher"],
            test_hands[poker_hand_value.name]["Middle"],
            test_hands[poker_hand_value.name]["Lower"]
        ] )

    def test_draw_high_card(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.HighCard)

    def test_draw_pair(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.Pair)

    def test_draw_two_pairs(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.TwoPairs)

    def test_draw_three_of_a_kind(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.ThreeOfAKind)

    def test_draw_straight(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.Straight)

    def test_draw_flush(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.Flush)

    @unittest.expectedFailure
    def test_draw_same(self):
        # pylint: disable=maybe-no-member
        self.shuffleAndConfirmHandsSorted([
            test_hands[PokerHandValue.Flush.name]["Spades"],
            test_hands[PokerHandValue.Flush.name]["Hearts"],
            test_hands[PokerHandValue.Flush.name]["Diamonds"],
            test_hands[PokerHandValue.Flush.name]["Clubs"]
        ] )

    def test_draw_full_house(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.FullHouse)

    def test_draw_four_of_a_kind(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.FourOfAKind)

    def test_draw_straight_flush(self):
        self.shuffleAndConfirmDrawSorted(PokerHandValue.StraightFlush)

#@unittest.skip("Disable for now")
class TestPokerHandSortingPerformance(unittest.TestCase):
    def test_time_to_sort(self):
        dealer = Dealer()
        random_hands = []
        # Benchmark on home PC only running this test:
        #  Hands  Times Sorted Time
        #     50        25000  10.538s, 10.529s, 11.253s
        number_of_hands_to_benchmark = 50
        number_of_times_to_sort_hands = 25000

        number_of_packs_to_benchmark = number_of_hands_to_benchmark / 10
        test_desc = str(number_of_hands_to_benchmark) + " hands " + str(number_of_times_to_sort_hands) + " times "
        _logger.debug("Benchmark start creating PokerHand objects: " + test_desc)
        for hand_string in dealer.deal_pack(number_of_packs_to_benchmark):
            random_hands.append(PokerHand(hand_string))
        _logger.debug("Benchmark end creating PokerHand objects: " + test_desc)

        _logger.debug("Benchmark now sorting: " + test_desc)
        number_of_times_sorted_hands = 0
        while number_of_times_sorted_hands < number_of_times_to_sort_hands:
            number_of_times_sorted_hands = number_of_times_sorted_hands + 1
            sorted(random_hands)
        _logger.debug("Benchmark end sorting: " + test_desc)

if __name__ == "__main__":
    _logger = logging.getLogger(__name__)
    logging.basicConfig(
        level = logging.DEBUG,
        format = '%(asctime)-15s - %(levelname)s - %(message)s'
    )
    _logger.info("Sortable Poker Hands Tests")
    _logger.info("Author: Ed Plant")
    #unittest.main()

    # Run a single test (comment/uncomment as needed)
    # https://stackoverflow.com/questions/15971735/running-a-single-test-from-unittest-testcase-via-the-command-line
    suite = unittest.TestSuite()
    #suite.addTest(TestPokerHandValue("test_high_card"))
    #suite.addTest(TestPokerHandValue("test_straight"))
    #suite.addTest(TestPokerHandSorting("test_pair_beats_high_card"))
    #suite.addTest(TestPokerHandSorting("test_draw_high_card"))
    #suite.addTest(TestPokerHandSorting("test_draw_pair"))
    #suite.addTest(TestPokerHandValue("test_pair"))
    suite.addTest(TestPokerHandSortingPerformance("test_time_to_sort"))
    runner = unittest.TextTestRunner()
    runner.run(suite)