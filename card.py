import logging

from card_value import CardValue
from card_suit  import CardSuit

class Card(object):
    def __init__(self, cardStr):
        _logger = logging.getLogger(__name__)
        #_logger.debug("Card init: " + cardStr)

        if len(cardStr) != 2:
            raise Exception(cardStr + " is not a valid card!")

        self.value = CardValue(cardStr[0])
        self.suit = CardSuit(cardStr[1])

    def get_suit(self):
        return self.suit

    def get_value(self):
        return self.value