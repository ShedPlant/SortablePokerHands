from ordered_enum import OrderedEnum

class PokerHandValue(OrderedEnum):
    StraightFlush =  "9"
    FourOfAKind   =  "8"
    FullHouse     =  "7"
    Flush         =  "6"
    Straight      =  "5"
    ThreeOfAKind  =  "4"
    TwoPairs      =  "3"
    Pair          =  "2"
    HighCard      =  "1"