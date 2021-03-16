from card_value import CardValue
from card_suit import CardSuit


class Card(object):
    def __repr__(self):
        return self.value.value + self.suit.value

    def __init__(self, card_as_string):
        if len(card_as_string) != 2:
            raise Exception(card_as_string + " is not a valid card!")

        # This will raise exception if input was invalid
        self.value = CardValue(card_as_string[0])
        self.suit = CardSuit(card_as_string[1])

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value

    def __lt__(self, other):
        return self.value < other.value
