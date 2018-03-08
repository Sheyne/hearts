import typing
from collections import namedtuple
from random import shuffle

Card = namedtuple("Card", "suit, number")
suits = "♠♥♣♦"
suit_order = "SHCD"
cards = [*[str(n) for n in range(2, 11)], "J", "Q", "K", "A"]

spades = suit_order.index("S")
hearts = suit_order.index("H")
clubs = suit_order.index("C")
diamonds = suit_order.index("D")
queen = cards.index("Q")
queen_spades = Card(spades, queen)

Card.__str__ = lambda self: cards[self.number]+suits[self.suit]

def str_hand(h: typing.List[Card], sort=True):
    if sort:
        h.sort()
    return " ".join(str(c) for c in h)

def score(pile: typing.List[Card]) -> int:
    return sum(1
        if card.suit == hearts else
        (13 if card == queen_spades else 0)
            for card in pile)

def valid_moves(hand: typing.List[Card], stack: typing.List[Card]) -> typing.List[Card]:
    if len(stack) == 0:
        return hand
    ret = [card for card in hand if card.suit == stack[0].suit]
    if len(ret) == 0:
        return hand
    return ret

all_cards = set(Card(suit, number)
    for suit in range(4)
        for number in range(13))

def chunks(l, n):
    c = len(l) // n
    for i in range(0, len(l), c):
        yield l[i:i + c]

def deal():
    deck = list(all_cards)
    shuffle(deck)
    return chunks(deck, 4)

def play(hand: typing.List[Card], card: Card, stacks: typing.List[typing.List[Card]]):
    hand.remove(card)
    stacks[-1].append(card)
    