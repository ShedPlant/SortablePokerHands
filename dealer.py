from card_value import CardValue
from card_suit  import CardSuit
from random import shuffle

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
            # hands.append(" ".join(pack[:5]))
            # hands.append(" ".join(pack[5:10]))
            # hands.append(" ".join(pack[10:15]))
            # hands.append(" ".join(pack[15:20]))
            # hands.append(" ".join(pack[20:25]))
            # hands.append(" ".join(pack[25:30]))
            # hands.append(" ".join(pack[30:35]))
            # hands.append(" ".join(pack[35:40]))
            # hands.append(" ".join(pack[40:45]))
            # hands.append(" ".join(pack[45:50]))
            # burn the last two cards

            number_of_packs_completed = number_of_packs_completed + 1
        return hands