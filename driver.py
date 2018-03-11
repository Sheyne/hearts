import hearts
import typing
from random import shuffle, randint


def choose_random(hand: typing.List[hearts.Card], stacks: typing.List[typing.List[hearts.Card]]) -> hearts.Card:
    valid = hearts.valid_moves(hand, stacks)
    return valid[randint(0, len(valid) - 1)]

def choose_smallest(hand: typing.List[hearts.Card], stacks: typing.List[typing.List[hearts.Card]]) -> hearts.Card:
    valid = hearts.valid_moves(hand, stacks)
    return min(valid, key=hearts.Card.number.fget)

def choose_largest(hand: typing.List[hearts.Card], stacks: typing.List[typing.List[hearts.Card]]) -> hearts.Card:
    valid = hearts.valid_moves(hand, stacks)
    return max(valid, key=hearts.Card.number.fget)

def choose_largest_except_spades(hand: typing.List[hearts.Card], stacks: typing.List[typing.List[hearts.Card]]) -> hearts.Card:
    valid = hearts.valid_moves(hand, stacks)
    if valid[0].suit == hearts.spades:
        return min(valid, key=hearts.Card.number.fget)
    return max(valid, key=hearts.Card.number.fget)

def bleed_spades(hand: typing.List[hearts.Card], stacks: typing.List[typing.List[hearts.Card]]) -> hearts.Card:
    valid = hearts.valid_moves(hand, stacks)
    spades = [c for c in valid if c.suit == hearts.spades]
    non_spades = [c for c in valid if c.suit != hearts.spades]
    safe_spades = [s for s in spades if s.number < hearts.queen]
    unsafe_spades = [s for s in spades if s.number >= hearts.queen]
    if unsafe_spades:
        if non_spades:
            return max(non_spades, key=hearts.Card.number.fget)
        elif safe_spades:
            return max(safe_spades)
        else:
            return max(valid)
    elif safe_spades:
        return max(safe_spades)

    return max(valid, key=hearts.Card.number.fget)

def bleed_spades2(hand: typing.List[hearts.Card], stacks: typing.List[typing.List[hearts.Card]]) -> hearts.Card:
    valid = hearts.valid_moves(hand, stacks)
    spades = [c for c in valid if c.suit == hearts.spades]
    non_spades = [c for c in valid if c.suit != hearts.spades]
    safe_spades = [s for s in spades if s.number < hearts.queen]
    unsafe_spades = [s for s in spades if s.number >= hearts.queen]
    if unsafe_spades:
        if non_spades:
            return max(non_spades, key=hearts.Card.number.fget)
        elif safe_spades:
            return min(safe_spades)
        else:
            return max(valid)
    elif safe_spades:
        return max(safe_spades)

    return max(valid, key=hearts.Card.number.fget)

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

def get_results(times=500):
    results = []

    for x in range(times):
        hands = list(zip(hearts.deal(), [bleed_spades, bleed_spades2, bleed_spades, bleed_spades]))

        stacks: typing.List[typing.List[hearts.Card]] = []
        starting_player = 0
        piles: typing.List[typing.List[hearts.Card]] = [[], [], [], []]
        must_play = None

        for player_idx, (hand, _) in enumerate(hands):
            try:
                must_play = hand.index(hearts.Card(hearts.clubs, 0))
                starting_player = player_idx
                break
            except ValueError:
                continue
        else:
            raise ValueError("2 of clubs not found") 

        while len(hands[0][0]) > 0:
            stacks.append([])
            max_play_idx = 0
            max_player_idx = starting_player

            # print("=" * 30)
            for play_idx, player_idx in enumerate(range(starting_player, starting_player + 4)):
                if must_play != None:
                    choice = hand[must_play]
                    must_play = None
                else:
                    player_idx = player_idx % 4
                    hand, chooser = hands[player_idx]
                    choice = chooser(hand, stacks)
                hearts.play(hand, choice, stacks)
                if choice.suit == stacks[-1][0].suit:
                    if choice.number > stacks[-1][max_play_idx].number:
                        max_play_idx = play_idx
                        max_player_idx = player_idx
            starting_player = max_player_idx
            for card in stacks[-1]:
                piles[max_player_idx].append(card)
        
        results.append(piles)
    return results


if __name__ == "__main__":
    results = get_results(100000)

    print("scoring")
    import numpy

    scores = numpy.array([
        [
            hearts.score(pile)
            for pile in result
        ]
        for result in results
    ])

    print(scores.mean(0))

    # for idx, pile in enumerate(piles):
    #     print(f"player {idx}: {hearts.str_hand(pile)}")
    #     print(f"= {hearts.score(pile)}")


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

