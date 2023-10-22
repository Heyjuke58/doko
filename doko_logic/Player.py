from functools import reduce

from rich.console import Console

from .Card import Card
from .GameModes import GameModus, Regular
from .Trick import Trick


class Player:
    def __init__(self, nr: int, name: str) -> None:
        self.nr = nr
        self.name = name

        self.hands: dict[int, list[Card]] = {}  # to store all hands a player had in a game
        self.hand: list[Card] = []  # current hand

        self.tricks_all: dict[int, list[Trick]] = {}  # to store all tricks a player got in a game
        self.tricks: list[Trick] = []  # current tricks the player got

        self.teams: list[int] = []  # to store all teams the player was in
        self.team: int = -1  # current team 0: Re 1: Contra 2: Undecided

        self.game_points = 0  # win points each player gets or loses after a game
        self.card_points: dict[int, int] = {}  # points of cards in every trick of a game

        self.console = Console()  # for logging hand

    def has_piggies(self, trump_color: int) -> bool:
        foxes = [card for card in self.hand if card == Card(trump_color, 0)]
        return len(foxes) == 2

    def has_wedding(self):
        re_queens = [card for card in self.hand if card == Card(0, 3)]
        return len(re_queens) == 2

    def is_re(self) -> bool:
        return any([card == Card(0, 3) for card in self.hand])

    def add_points(self, amount: int) -> None:
        self.game_points += amount

    def set_team(self, team: int) -> None:
        self.team = team

    def set_hand(self, hand: list[Card]) -> None:
        assert len(hand) in {10, 12}, "Invalid number of hand cards."
        self.hand = self.sort_hand(hand)

    # TODO: sort hand differently when player has piggies
    @staticmethod
    def sort_hand(hand: list[Card], game_modus: GameModus = Regular()):
        trumps = [(card, idx, game_modus.trumps.index(card)) for idx, card in enumerate(hand) if card in game_modus.trumps]
        trumps.sort(key=lambda x: x[2])  # sort by trump index
        non_trumps = [(card, idx) for card, idx in zip(hand, game_modus.trumps) if not card in game_modus.trumps]
        non_trumps.sort(key=lambda x: x[0])  # sort non trump cards by symbol and color
        sorted_hand = [card for card, _, __ in trumps]
        sorted_hand.extend([card for card, _ in non_trumps])
        return sorted_hand

    def final_hand_sort(self, game_modus: GameModus, game_nr: int):
        sorted_hand = self.sort_hand(self.hand, game_modus)
        self.hand = sorted_hand
        self.hands[game_nr] = sorted_hand

    def handle_poverty(self, receiving_cards: list[Card], losing_cards: list[Card]) -> None:
        for card in losing_cards:
            self.hand.remove(card)
        self.hand.extend(receiving_cards)

    def get_hand_str(self) -> str:
        hand_str = str([str(idx) + ": " + card.__str__() for idx, card in enumerate(self.hand)])
        return hand_str

    def play_card(self, nr: int) -> Card:
        return self.hand.pop(nr)

    def receive_trick(self, trick: Trick) -> None:
        self.tricks.append(trick)
        if not trick.nr in self.card_points:
            self.card_points[trick.nr] = 0
        self.card_points[trick.nr] += reduce(lambda x, y: x + y, [card.get_value() for card in trick.cards])

    def store_game(self, game_nr: int) -> None:
        self.tricks_all[game_nr] = self.tricks
        self.tricks = []
        self.teams.append(self.team)
        self.team = -1
