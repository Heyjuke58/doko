from dataclasses import dataclass
from typing import Annotated, Optional

from .Card import Card


@dataclass
class Trick:
    nr: int  # trick number within one game (0-9 in normal and 0-11 with nines)
    game_nr: int  # game number of the trick
    cards: Annotated[list[Card], 4]  # played cards
    players: Annotated[list[int], 4]  # index: card, value: player
    teams: Annotated[list[int], 4]  # index: player, value: team (0: Re, 1: Contra, 2: Neither)
    receiving_player: int = -1  # -1 indicastes that there is not yet a player receiving the trick

    def set_receiving_player(self, player: int) -> None:
        self.receiving_player = player

    def __str__(self):
        return str([str(card) for card in self.cards])
