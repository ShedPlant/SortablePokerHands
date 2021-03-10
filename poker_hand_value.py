from ordered_enum import OrderedEnum

class PokerHandValue(OrderedEnum):
    HighCard      =  "1"
    Pair          =  "2"
    TwoPairs      =  "3"
    ThreeOfAKind  =  "4"
    Straight      =  "5"
    Flush         =  "6"
    FullHouse     =  "7"
    FourOfAKind   =  "8"
    StraightFlush =  "9"
    RoyalFlush    = "10"

    def get_draw_sorting_type(self):
        simply_sorted_hand_types = [
            PokerHandValue.RoyalFlush,
            PokerHandValue.StraightFlush,
            PokerHandValue.Flush,
            PokerHandValue.Straight,
            PokerHandValue.HighCard
        ]
        one_group_hand_types = [
            PokerHandValue.FourOfAKind,
            PokerHandValue.ThreeOfAKind,
            PokerHandValue.Pair
        ]
        two_group_hand_types = [
            PokerHandValue.FullHouse,
            PokerHandValue.TwoPairs
        ]
        if self in simply_sorted_hand_types:
            return "all"
        elif self in one_group_hand_types:
            return "one_group"
        elif self in two_group_hand_types:
            return "two_groups"
        else:
            NotImplemented