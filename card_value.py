from ordered_enum import OrderedEnum

class CardValue(OrderedEnum):
    Two    = '2'
    Three  = '3'
    Four   = '4'
    Five   = '5'
    Six    = '6'
    Seven  = '7'
    Eight  = '8'
    Nine   = '9'
    Ten    = 'T'
    Jack   = 'J'
    Queen  = 'Q'
    King   = 'K'
    Ace    = 'A'

    # Adapted / extended https://github.com/woodruffw/ordered_enum/blob/master/src/ordered_enum/ordered_enum.py
    def __sub__(self, other):
        if self.__class__ is other.__class__:
            member_list = self.__class__._member_list()
            return member_list.index(self) - member_list.index(other)
        return NotImplemented