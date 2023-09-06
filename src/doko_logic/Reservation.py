from dataclasses import dataclass
from typing import Optional

from GameModes import (ColorSoloDiamondsReplaced,
                       ColorSoloDiamondsReplacedWithPiggies, ColorSoloPure,
                       GameModus, JacksSolo, KingsSolo, Meatless,
                       QueensJacksSolo, QueensSolo, SilentWedding,
                       SilentWeddingWithPiggies, TrumpSolo,
                       TrumpSoloWithPiggies)
from Player import Player
from Rules import Rules

RESERVATION_VALUES = {
    0: 'fine',
    1: 'wedding',
    2: 'poverty',
    3: 'solo',
    4: 'throw'
}

SOLO_VALUES = {
    0: SilentWedding,
    1: TrumpSolo,
    2: 'ColorSolo',
    3: QueensSolo,
    4: JacksSolo,
    5: KingsSolo,
    6: QueensJacksSolo,
    7: Meatless
}

@dataclass
class Reservation:
    value: int
    player: int
    play_piggies: bool = False
    solo: Optional[int] = None
    color_solo_color: Optional[int] = None

    def is_sound(self):
        return self.value == 0

    def is_wedding(self):
        return self.value == 1
    
    def is_silent_wedding(self):
        return self.value == 3 and self.solo == 0

    def is_poverty(self):
        return self.value == 2

    def is_solo(self):
        return self.value == 3 and self.solo != 0 # silent wedding is not announced as solo

    def is_throw(self):
        return self.value == 4

    def get_solo(self, players: list[Player], rules: Rules) -> GameModus:
        assert self.solo is not None, "No solo announced"

        if self.solo == 0:
            if any([player.has_piggies(trump_color=3) for player in players]) and rules.piggies:
                return SilentWeddingWithPiggies()
            
        if self.solo == 1:
            if any([player.has_piggies(trump_color=3) for player in players]) and rules.piggies_in_trump_and_color_solo:
                return TrumpSoloWithPiggies()
            
        if self.solo == 2 and self.color_solo_color is not None:
            if rules.color_solo_pure:
                return ColorSoloPure(color=self.color_solo_color)
            else:
                if any([player.has_piggies(trump_color=self.color_solo_color) for player in players]) and rules.piggies_in_trump_and_color_solo:
                    return ColorSoloDiamondsReplacedWithPiggies(color=self.color_solo_color)
                else:
                    return ColorSoloDiamondsReplaced(color=self.color_solo_color)
        
        return SOLO_VALUES[self.solo]()
    