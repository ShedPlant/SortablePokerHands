# Python Software Engineering Challenge
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

# Reflections
I created a class model:
- CardValue
- CardSuit
- Card
- PokerHandValue
- PokerHand
- Dealer (randomly creates hands)

Regression tests cover:
- Input validation error handling
- all hand types identified appropriately
- sorting hands of different hand types (e.g. pair beats high card)
- sorting hands within same type (e.g. pair of 3s beats pair of 2s)
- low ace straight special case
- performance benchmarking of many hands at once

My phases of thinking were:
- basic class structure and input error validation
- to identify each hand type
- compare one hand with another where the hand type differes
- then think about draws within same type

By that point, I had something that functionally worked but didn't perform very well. It timed out on CodeWars. So I created a benchmark test: 17s to create and sort 10^6 random hands.
With my fuller understanding of the problem, I went back and started again with a simpler sorting approach that worked whether the hand value were different or the same.
Reduced benchmark to about 9s.
However it still times out on the CodeWars full random tests. I'm a little disappointed!

I really enjoyed working on this assignment. I spent about 2 days on it in total.

I would really appreciate any review comments and feedback about any aspects I did well or not so well.
