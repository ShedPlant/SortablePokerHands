from ordered_enum import OrderedEnum

class CardValue(OrderedEnum):
    Ace    = 'A'
    King   = 'K'
    Queen  = 'Q'
    Jack   = 'J'
    Ten    = 'T'
    Nine   = '9'
    Eight  = '8'
    Seven  = '7'
    Six    = '6'
    Five   = '5'
    Four   = '4'
    Three  = '3'
    Two    = '2'
    AceLow = 'a'

    # Copied and extended
    # https://github.com/woodruffw/ordered_enum/blob/master/src/ordered_enum/ordered_enum.py
    # to add sub
    def __sub__(self, other):
        if self.__class__ is other.__class__:
            member_list = self.__class__._member_list()
            return member_list.index(self) - member_list.index(other)
        return NotImplemented