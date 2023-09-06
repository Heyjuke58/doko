from Card import Card
from GameModes import GameModus, Regular
from Reservation import Reservation
from Sitting import Sitting
from Trick import Trick

all_fine_hands: list[list[Card]] = [
    [Card(0, 0), Card(0, 0), Card(0, 1), Card(0, 1), Card(0, 2), Card(0, 2), Card(1, 3), Card(0, 3), Card(0, 4), Card(0, 4)],
    [Card(1, 0), Card(1, 0), Card(1, 1), Card(1, 1), Card(1, 2), Card(1, 2), Card(1, 3), Card(0, 3), Card(1, 4), Card(1, 4)],
    [Card(3, 0), Card(2, 0), Card(2, 1), Card(2, 1), Card(2, 2), Card(2, 2), Card(2, 3), Card(2, 3), Card(2, 4), Card(2, 4)],
    [Card(3, 0), Card(2, 0), Card(3, 1), Card(3, 1), Card(3, 2), Card(3, 2), Card(3, 3), Card(3, 3), Card(3, 4), Card(3, 4)],
]

wedding_hands: list[list[Card]] = [
    [Card(0, 0), Card(0, 0), Card(0, 1), Card(0, 1), Card(0, 2), Card(0, 2), Card(0, 3), Card(0, 3), Card(0, 4), Card(0, 4)],
    [Card(1, 0), Card(1, 0), Card(1, 1), Card(1, 1), Card(1, 2), Card(1, 2), Card(1, 3), Card(1, 3), Card(1, 4), Card(1, 4)],
    [Card(3, 0), Card(2, 0), Card(2, 1), Card(2, 1), Card(2, 2), Card(2, 2), Card(2, 3), Card(2, 3), Card(2, 4), Card(2, 4)],
    [Card(3, 0), Card(2, 0), Card(3, 1), Card(3, 1), Card(3, 2), Card(3, 2), Card(3, 3), Card(3, 3), Card(3, 4), Card(3, 4)],
]


def standard_test_setup(**kwargs):
    sitting = Sitting(player_names=["Alphons", "Beate", "Gabi", "Detmar"], **kwargs)

    return sitting


def standard_test_setup_all_fine(**kwargs):
    sitting = Sitting(player_names=["Alphons", "Beate", "Gabi", "Detmar"], **kwargs)
    sitting.deal_cards(all_fine_hands)
    reservations = [
        Reservation(value=0, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, _ = sitting.evaluate_reservations(reservations)
    return sitting, game_modus


class SittingTest:
    def __init__(self, sitting: Sitting, game_modus: GameModus = Regular()) -> None:
        self.sitting = sitting
        self.game_modus = game_modus

    def play_trick(self, trick: Trick):
        self.sitting.evaluate_trick(trick, self.game_modus)
