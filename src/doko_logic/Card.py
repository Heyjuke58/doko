from dataclasses import dataclass

COLORS = {0: "clubs", 1: "spades", 2: "hearts", 3: "diamonds"}

COLORSYMBOLS = {0: "\u2663", 1: "\u2660", 2: "\u2665", 3: "\u2666"}

SYMBOLS = {0: "ace", 1: "ten", 2: "king", 3: "queen", 4: "jack", 5: "nine"}

SHORTSYMBOLS = {0: "A", 1: "10", 2: "K", 3: "Q", 4: "J", 5: "9"}

VALUES = {0: 11, 1: 10, 2: 4, 3: 3, 4: 2, 5: 0}


@dataclass
class Card:
    color: int
    symbol: int

    def get_symbol_str(self):
        return SYMBOLS[self.symbol]

    def get_color_str(self):
        return COLORS[self.color]

    def get_value(self):
        return VALUES[self.symbol]

    def __str__(self) -> str:
        return COLORSYMBOLS[self.color] + " " + SHORTSYMBOLS[self.symbol]

    def is_dulle(self) -> bool:
        return self.symbol == 1 and self.color == 2

    def __eq__(self, other):
        if not isinstance(other, Card):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.symbol == other.symbol and self.color == other.color

    def __lt__(self, other: "Card"):
        if not isinstance(other, Card):
            # don't attempt to compare against unrelated types
            return NotImplemented

        if self.color < other.color:
            return True
        elif self.color > other.color:
            return False
        else:
            return self.symbol < other.symbol
