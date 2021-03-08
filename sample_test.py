from random import shuffle
from itertools import chain

Test.describe("Sample tests")

SORTED_POKER_HANDS = list(map(PokerHand, ["KS AS TS QS JS",
                                          "2H 3H 4H 5H 6H",
                                          "AS AD AC AH JD",
                                          "JS JD JC JH 3D",
                                          "2S AH 2H AS AC",
                                          "AS 3S 4S 8S 2S",
                                          "2H 3H 5H 6H 7H",
                                          "2S 3H 4H 5S 6C",
                                          "2D AC 3H 4H 5S",
                                          "AH AC 5H 6H AS",
                                          "2S 2H 4H 5S 4C",
                                          "AH AC 5H 6H 7S",
                                          "AH AC 4H 6H 7S",
                                          "2S AH 4H 5S KC",
                                          "2S 3H 6H 7S 9C"]))

Test.it("Sorting Tests")

lstCopy = SORTED_POKER_HANDS.copy()
shuffle(lstCopy)
userSortedHands = chain(sorted(lstCopy))

for hand in SORTED_POKER_HANDS:
    test.assert_equals(next(userSortedHands), hand)
