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
            PokerHandValue.Flush,
            PokerHandValue.HighCard
        ]
        check_for_low_ace = [
            PokerHandValue.Straight,
            PokerHandValue.StraightFlush
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
            return "high_to_low"
        elif self in check_for_low_ace:
            return "high_to_low_ace_can_be_low"
        elif self in one_group_hand_types:
            return "one_group_then_kickers"
        elif self in two_group_hand_types:
            return "two_groups_then_kickers"
        else:
            NotImplemented