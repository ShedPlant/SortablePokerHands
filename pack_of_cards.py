from random import shuffle
from card_value import CardValue
from card_suit  import CardSuit

class PackOfCards(list):
    def __new__(self):
        cards = []
        for suit in list(CardSuit):
            for card_value in list(CardValue):
                if card_value.name != "ACE_LOW":
                    cards.append(card_value.value + suit.value)
        shuffle(cards)
        return cards