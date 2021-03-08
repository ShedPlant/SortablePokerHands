from poker_hand import PokerHand
import logging

_logger = logging.getLogger(__name__)
logging.basicConfig(
    level = logging.DEBUG,
    format = '%(asctime)-15s - %(levelname)s - %(message)s'
)
_logger.info("Sortable Poker Hands")
_logger.info("Author: Ed Plant")
_logger.debug("EJP debug")

myHand = PokerHand("KS AS TS QS JS")