from enum import Enum
# Adapted from
# https://docs.python.org/3/library/enum.html#planet
# 
# CardValue has two attributes:
# value = a single character string, might be a number or a letter. 
#         Used for lookups
# score = an integer score. May or may not be int representation of 'value'
class CardValue(Enum):
    def __new__(cls, value):
        # Scores are assigned automatically by order listed
        # starting with 1
        score = len(cls.__members__) + 1
        obj = object.__new__(cls)

        # Value is a single character string 
        # used for Enum lookups e.g. CardValue('5')
        obj._value_ = value
        # This variable can only be exposed by property method below
        # can't use the same exact variable name
        obj._score_ = score
        return obj

    @property
    # Score is an integer value
    def score(self):
        return self._score_

    def __lt__(self, other):
        return self.score < other.score

    def __sub__(self, other):
        return self.score - other.score

    ACE_LOW = 'a'
    TWO     = '2'
    THREE   = '3'
    FOUR    = '4'
    FIVE    = '5'
    SIX     = '6'
    SEVEN   = '7'
    EIGHT   = '8'
    NINE    = '9'
    TEN     = 'T'
    JACK    = 'J'
    QUEEN   = 'Q'
    KING    = 'K'
    ACE     = 'A'