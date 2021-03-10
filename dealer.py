from card_value import CardValue
from card_suit  import CardSuit
from random import shuffle

"""
 Create a number of pack of cards
 Shuffle each one and deal into 5 card hands, throw away the 2 remaining
 Return the list of hands

 Useful for benchmarking / random testing
"""
class Dealer():
    def deal_pack(self, number_of_packs):
        hands = []
        pack = []
        number_of_packs_completed = 0
        for suit in list(CardSuit):
            for card_value in list(CardValue):
                if card_value.value != 'a':
                    pack.append(card_value.value + suit.value)

        while number_of_packs_completed < number_of_packs:
            shuffle(pack)
            start_index = 0
            end_index = 5
            while end_index < 50:
                hands.append(" ".join(pack[start_index:end_index]))
                start_index = start_index + 5
                end_index = end_index + 5
            # burn the last two cards to make round number

            number_of_packs_completed = number_of_packs_completed + 1
        return hands