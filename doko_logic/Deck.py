from .Card import COLORS, SYMBOLS, Card


class Deck:
    def __init__(self, nines: bool) -> None:
        self.cards = []
        if nines:
            for _ in range(2):
                for color in COLORS:
                    for symbol in SYMBOLS:
                        self.cards.append(Card(color, symbol))
        else:
            for _ in range(2):
                for color in COLORS:
                    for symbol in list(SYMBOLS)[:-1]:
                        self.cards.append(Card(color, symbol))
