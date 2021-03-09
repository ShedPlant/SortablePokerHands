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