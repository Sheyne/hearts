import hearts
import typing
from random import shuffle


def choose_random(hand: typing.List[hearts.Card], stacks: typing.List[typing.List[hearts.Card]]) -> hearts.Card:
    valid = hearts.valid_moves(hand, stacks)
    shuffle(valid)
    return valid[0]

def choose_human(hand: typing.List[hearts.Card], stacks: typing.List[typing.List[hearts.Card]]) -> hearts.Card:
    print(f"stack: {hearts.str_hand(stacks[-1], sort=False)}")
    print(f"hand: {hearts.str_hand(hand)}")
    valid: typing.Set[hearts.Card] = set(hearts.valid_moves(hand, stacks))
    card = None

    while card not in valid:
        *n_strs, s_str = input("choice (5H): ").upper()
        s = hearts.suit_order.index(s_str)
        n = hearts.cards.index("".join(n_strs))
        card = hearts.Card(s, n)
    
    return typing.cast(hearts.Card, card)

hands = list(zip(hearts.deal(), [choose_human, choose_random, choose_random, choose_random]))

stacks: typing.List[typing.List[hearts.Card]] = []
starting_player = 0
piles: typing.List[typing.List[hearts.Card]] = [[], [], [], []]
while len(hands[0][0]) > 0:
    stacks.append([])
    max_play_idx = 0
    max_player_idx = starting_player
    print("=" * 30)
    for play_idx, player_idx in enumerate(range(starting_player, starting_player + 4)):
        player_idx = player_idx % 4
        hand, chooser = hands[player_idx]
        choice = chooser(hand, stacks)
        print(f"player {player_idx}: {hearts.str_hand([choice])}")
        hearts.play(hand, choice, stacks)
        if choice.suit == stacks[-1][0].suit:
            if choice.number > stacks[-1][max_play_idx].number:
                max_play_idx = play_idx
                max_player_idx = player_idx
    starting_player = max_player_idx
    for card in stacks[-1]:
        piles[max_player_idx].append(card)
    
for idx, pile in enumerate(piles):
    print(f"player {idx}: {hearts.str_hand(pile)}")
    print(f"= {hearts.score(pile)}")


# def evaluate(card: Card, hand: typing.List[Card], stacks: typing.List[typing.List[Card]]) -> int:
#     cards = set(hand) | set(card
#         for stack in stacks
#             for card in stack)
#     other_cards = list(all_cards - cards)
#     shuffle(other_cards)
#     # play(card, stacks)
#     return -card.number

# def choose(hand: typing.List[Card], stacks: typing.List[typing.List[Card]]):
#     evaluations = [(evaluate(card, hand, stacks), card)
#                     for card in valid_moves(hand, stacks[-1])]
#     return min(evaluations)[1]

