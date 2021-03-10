# ***REMOVED*** Python Software Engineering Challenge
## Ed Plant, March 2021

# Assignment
 
[CodeWars SortablePokerHands](https://www.codewars.com/kata/586423aa39c5abfcec0001e6/train/python)

A famous casino is suddenly faced with a sharp decline of their revenues.
They decide to offer Texas hold'em also online.
Can you help them by writing an algorithm that can rank poker hands?

Task:

Create a poker hand that has a constructor that accepts a string containing 5 cards:
```python
hand = PokerHand("KS 2H 5C JD TD")
```
The characteristics of the string of cards are:
A space is used as card seperator
Each card consists of two characters
The first character is the value of the card, valid characters are:
```python
2, 3, 4, 5, 6, 7, 8, 9, T(en), J(ack), Q(ueen), K(ing), A(ce)
```
The second character represents the suit, valid characters are:
```python
S(pades), H(earts), D(iamonds), C(lubs)
```

The poker hands must be sortable by rank, the highest rank first:
```python
hands = []
hands.append(PokerHand("KS 2H 5C JD TD"))
hands.append(PokerHand("2C 3C AC 4C 5C"))
hands.sort() (or sorted(hands))
```
Apply the Texas Hold'em rules for ranking the cards.
There is no ranking for the suits.
An ace can either rank high or rank low in a straight or straight flush. Example of a straight with a low ace:
`"5C 4D 3C 2S AS"`

Note: there are around 25000 random tests, so keep an eye on performances.

https://en.wikipedia.org/wiki/Texas_hold_%27em
https://en.wikipedia.org/wiki/List_of_poker_hands

