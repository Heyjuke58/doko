import abc

from Card import Card

REGULAR_TRUMP_ORDER = [
    Card(color=2, symbol=1),  # Dulle
    Card(color=0, symbol=3),  # Queen of clubs
    Card(color=1, symbol=3),  # Queen of spades
    Card(color=2, symbol=3),  # Queen of hearts
    Card(color=3, symbol=3),  # Queen of diamonds
    Card(color=0, symbol=4),  # Jack of clubs
    Card(color=1, symbol=4),  # Jack of spades
    Card(color=2, symbol=4),  # Jack of hearts
    Card(color=3, symbol=4),  # Jack of diamonds
    Card(color=3, symbol=0),  # Ace of diamonds
    Card(color=3, symbol=1),  # Ten of diamonds
    Card(color=3, symbol=2),  # King of diamonds
    Card(color=3, symbol=5),  # Nine of diamonds
]

PIGGIES_TRUMP_ORDER = [
    Card(color=3, symbol=0),  # Ace of diamonds
    Card(color=2, symbol=1),  # Dulle
    Card(color=0, symbol=3),  # Queen of clubs
    Card(color=1, symbol=3),  # Queen of spades
    Card(color=2, symbol=3),  # Queen of hearts
    Card(color=3, symbol=3),  # Queen of diamonds
    Card(color=0, symbol=4),  # Jack of clubs
    Card(color=1, symbol=4),  # Jack of spades
    Card(color=2, symbol=4),  # Jack of hearts
    Card(color=3, symbol=4),  # Jack of diamonds
    Card(color=3, symbol=1),  # Ten of diamonds
    Card(color=3, symbol=2),  # King of diamonds
    Card(color=3, symbol=5),  # Nine of diamonds
]


class GameModus(abc.ABC):
    def __init__(self, name: str, trumps: list[Card]) -> None:
        super().__init__()
        self.name = name
        self.trumps = trumps  # in order highest -> lowest

    def is_trump(self, card: Card):
        return any([card == t for t in self.trumps])


class Regular(GameModus):
    def __init__(self) -> None:
        super().__init__("Regular", REGULAR_TRUMP_ORDER)


class Piggies(GameModus):
    def __init__(self) -> None:
        super().__init__("Piggies", PIGGIES_TRUMP_ORDER)


class Poverty(GameModus):
    def __init__(self) -> None:
        super().__init__("Poverty", REGULAR_TRUMP_ORDER)


class PovertyWithPiggies(GameModus):
    def __init__(self) -> None:
        super().__init__("Poverty with piggies", PIGGIES_TRUMP_ORDER)


class Wedding(GameModus):
    def __init__(self) -> None:
        super().__init__("Wedding", REGULAR_TRUMP_ORDER)


class WeddingWithPiggies(GameModus):
    def __init__(self) -> None:
        super().__init__("Wedding with piggies", PIGGIES_TRUMP_ORDER)


## SOLOS ##
class Solo(GameModus):
    def __init__(self, name: str, trumps: list[Card]) -> None:
        super().__init__(name, trumps)


class SilentWedding(Solo):
    def __init__(self) -> None:
        super().__init__("Silent wedding", REGULAR_TRUMP_ORDER)


class SilentWeddingWithPiggies(Solo):
    def __init__(self) -> None:
        super().__init__("Silent wedding with piggies", PIGGIES_TRUMP_ORDER)


class TrumpSolo(Solo):
    def __init__(self) -> None:
        super().__init__("Trump solo", REGULAR_TRUMP_ORDER)


class TrumpSoloWithPiggies(Solo):
    def __init__(self) -> None:
        super().__init__("Trump solo with piggies", PIGGIES_TRUMP_ORDER)


class ColorSoloPure(Solo):
    def __init__(self, color: int) -> None:
        trumps = [
            Card(color=color, symbol=0),  # Ace
            Card(color=color, symbol=1),  # Ten
            Card(color=color, symbol=2),  # King
            Card(color=color, symbol=3),  # Queen
            Card(color=color, symbol=4),  # Jack
            Card(color=color, symbol=5),  # Nine
        ]
        super().__init__("Pure color solo", trumps)


class ColorSoloDiamondsReplaced(Solo):
    def __init__(self, color: int) -> None:
        self.color = color
        trumps = [
            Card(color=2, symbol=1),  # Dulle
            Card(color=0, symbol=3),  # Queen of clubs
            Card(color=1, symbol=3),  # Queen of spades
            Card(color=2, symbol=3),  # Queen of hearts
            Card(color=3, symbol=3),  # Queen of diamonds
            Card(color=0, symbol=4),  # Jack of clubs
            Card(color=1, symbol=4),  # Jack of spades
            Card(color=2, symbol=4),  # Jack of hearts
            Card(color=3, symbol=4),  # Jack of diamonds
            Card(color=color, symbol=0),  # Ace
            Card(color=color, symbol=1),  # Ten
            Card(color=color, symbol=2),  # King
            Card(color=color, symbol=5),  # Nine
        ]
        super().__init__("Color solo diamonds replaced", trumps)


class ColorSoloDiamondsReplacedWithPiggies(Solo):
    def __init__(self, color: int) -> None:
        self.color = color
        trumps = [
            Card(color=color, symbol=0),  # Ace
            Card(color=2, symbol=1),  # Dulle
            Card(color=0, symbol=3),  # Queen of clubs
            Card(color=1, symbol=3),  # Queen of spades
            Card(color=2, symbol=3),  # Queen of hearts
            Card(color=3, symbol=3),  # Queen of diamonds
            Card(color=0, symbol=4),  # Jack of clubs
            Card(color=1, symbol=4),  # Jack of spades
            Card(color=2, symbol=4),  # Jack of hearts
            Card(color=3, symbol=4),  # Jack of diamonds
            Card(color=color, symbol=1),  # Ten
            Card(color=color, symbol=2),  # King
            Card(color=color, symbol=5),  # Nine
        ]
        super().__init__("Color solo diamonds replaced with piggies", trumps)


class QueensSolo(Solo):
    def __init__(self) -> None:
        trumps = [
            Card(color=0, symbol=3),  # Queen of clubs
            Card(color=1, symbol=3),  # Queen of spades
            Card(color=2, symbol=3),  # Queen of hearts
            Card(color=3, symbol=3),  # Queen of diamonds
        ]
        super().__init__("Queens solo", trumps)


class JacksSolo(Solo):
    def __init__(self) -> None:
        trumps = [
            Card(color=0, symbol=4),  # Jack of clubs
            Card(color=1, symbol=4),  # Jack of spades
            Card(color=2, symbol=4),  # Jack of hearts
            Card(color=3, symbol=4),  # Jack of diamonds
        ]
        super().__init__("Jacks solo", trumps)


class KingsSolo(Solo):
    def __init__(self) -> None:
        trumps = [
            Card(color=0, symbol=2),  # King of clubs
            Card(color=1, symbol=2),  # King of spades
            Card(color=2, symbol=2),  # King of hearts
            Card(color=3, symbol=2),  # King of diamonds
        ]
        super().__init__("Kings solo", trumps)


class QueensJacksSolo(Solo):
    def __init__(self) -> None:
        trumps = [
            Card(color=0, symbol=3),  # Queen of clubs
            Card(color=1, symbol=3),  # Queen of spades
            Card(color=2, symbol=3),  # Queen of hearts
            Card(color=3, symbol=3),  # Queen of diamonds
            Card(color=0, symbol=4),  # Jack of clubs
            Card(color=1, symbol=4),  # Jack of spades
            Card(color=2, symbol=4),  # Jack of hearts
            Card(color=3, symbol=4),  # Jack of diamonds
        ]
        super().__init__("Queens and jacks solo", trumps)


class Meatless(Solo):
    def __init__(self) -> None:
        super().__init__("Meatless", [])


NON_SOLO_GAME_MODES = [
    Regular,
    Poverty,
    Wedding,
    Piggies,
    PovertyWithPiggies,
    WeddingWithPiggies,
]
SILENT_WEDDING_GAME_MODES = [
    SilentWedding,
    SilentWeddingWithPiggies,
]
TRUMP_SOLO_GAME_MODES = [
    TrumpSolo,
    TrumpSoloWithPiggies,
]
COLOR_SOLO_DIAMONDS_REPLACED_GAME_MODES = [
    ColorSoloDiamondsReplaced,
    ColorSoloDiamondsReplacedWithPiggies,
]
