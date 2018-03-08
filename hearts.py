import typing
from random import shuffle

T = typing.TypeVar('T')

suits = "♠♥♣♦"
suit_order = "SHCD"
cards: typing.List[str] = [*[str(n) for n in range(2, 11)], "J", "Q", "K", "A"]

spades = suit_order.index("S")
hearts = suit_order.index("H")
clubs = suit_order.index("C")
diamonds = suit_order.index("D")
queen = cards.index("Q")

class Card(typing.NamedTuple("Card", (("suit", int), ("number", int)))):
    __slots__ = ()
    def __str__(self) -> str:
        return cards[self.number]+suits[self.suit]

queen_spades = Card(spades, queen)

def str_hand(h: typing.List[Card], sort:bool=True) -> str:
    if sort:
        h.sort()
    return " ".join(str(c) for c in h)

def score(pile: typing.List[Card]) -> int:
    return sum(1
        if card.suit == hearts else
        (13 if card == queen_spades else 0)
            for card in pile)

def is_point_card(card: Card) -> bool:
    return card.suit == hearts or card == queen_spades

def valid_moves(hand: typing.List[Card], stacks: typing.List[typing.List[Card]]) -> typing.List[Card]:
    stack = stacks[-1]
    if len(stack) == 0:
        points_broken = any(is_point_card(card)
                            for stack in stacks
                                for card in stack)
        if points_broken:
            return hand
        else:
            return [card for card in hand if not is_point_card(card)]
    ret = [card for card in hand if card.suit == stack[0].suit]
    if len(ret) == 0:
        if len(stacks) == 1:
            non_point_cards = [card for card in hand if not is_point_card(card)]
            if non_point_cards:
                return non_point_cards
        return hand
    return ret

all_cards = set(Card(suit, number)
    for suit in range(4)
        for number in range(13))

def chunks(l : typing.List[T], n: int) -> typing.Iterable[typing.List[T]]:
    c = len(l) // n
    for i in range(0, len(l), c):
        yield l[i:i + c]

def deal() -> typing.Iterable[typing.List[Card]]:
    deck = list(all_cards)
    shuffle(deck)
    return chunks(deck, 4)

def play(hand: typing.List[Card], card: Card, stacks: typing.List[typing.List[Card]]) -> None:
    hand.remove(card)
    stacks[-1].append(card)
    