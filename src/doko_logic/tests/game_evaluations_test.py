import inspect
import os
import sys

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from Announcement import Announcement
from Card import Card
from tests.standard_setup import all_fine_hands, standard_test_setup, standard_test_setup_all_fine, wedding_hands
from Trick import Trick

all_fine_hands: list[list[Card]] = [
    [Card(0, 0), Card(0, 0), Card(0, 1), Card(0, 1), Card(2, 2), Card(3, 2), Card(1, 3), Card(0, 3), Card(0, 4), Card(0, 4)],
    [Card(1, 0), Card(1, 0), Card(1, 1), Card(1, 1), Card(2, 2), Card(3, 2), Card(1, 3), Card(0, 3), Card(1, 4), Card(1, 4)],
    [Card(3, 0), Card(2, 0), Card(2, 1), Card(2, 1), Card(0, 2), Card(1, 2), Card(2, 3), Card(2, 3), Card(2, 4), Card(2, 4)],
    [Card(3, 0), Card(2, 0), Card(3, 1), Card(3, 1), Card(0, 2), Card(1, 2), Card(3, 3), Card(3, 3), Card(3, 4), Card(3, 4)],
]


def test_re_win_annoucement():
    sitting, game_modus = standard_test_setup_all_fine()
    sitting.make_announcement(player_nr=0, announcement=Announcement(stage=0, team=0))
    tricks = [
        Trick(nr=0, game_nr=0, cards=[Card(0, 0), Card(1, 1), Card(0, 2), Card(0, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=1, game_nr=0, cards=[Card(0, 0), Card(1, 4), Card(2, 3), Card(2, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=2, game_nr=0, cards=[Card(0, 4), Card(1, 4), Card(2, 1), Card(3, 3)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=3, game_nr=0, cards=[Card(2, 2), Card(2, 2), Card(2, 0), Card(3, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=4, game_nr=0, cards=[Card(0, 3), Card(0, 3), Card(2, 4), Card(3, 3)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=5, game_nr=0, cards=[Card(0, 1), Card(1, 3), Card(2, 3), Card(3, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=6, game_nr=0, cards=[Card(0, 1), Card(1, 0), Card(1, 2), Card(1, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=7, game_nr=0, cards=[Card(3, 2), Card(1, 0), Card(2, 1), Card(3, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        # fox caught
        Trick(nr=8, game_nr=0, cards=[Card(1, 3), Card(1, 1), Card(3, 0), Card(3, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        # karlchen
        Trick(nr=9, game_nr=0, cards=[Card(0, 4), Card(3, 2), Card(2, 4), Card(3, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
    ]
    for trick in tricks:
        sitting.evaluate_trick(trick, game_modus)

    sitting.evaluate_game(0, game_modus)

    assert sitting.points[0] == sitting.points[1] == 5
    assert sitting.points[2] == sitting.points[3] == -5
    assert len(sitting.extra_points) == 2


def test_re_wrong_annoucement():
    sitting, game_modus = standard_test_setup_all_fine()
    sitting.make_announcement(player_nr=0, announcement=Announcement(stage=1, team=0))
    tricks = [
        Trick(nr=0, game_nr=0, cards=[Card(0, 0), Card(1, 1), Card(0, 2), Card(0, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=1, game_nr=0, cards=[Card(0, 0), Card(1, 4), Card(2, 3), Card(2, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=2, game_nr=0, cards=[Card(0, 4), Card(1, 4), Card(2, 1), Card(3, 3)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=3, game_nr=0, cards=[Card(2, 2), Card(2, 2), Card(2, 0), Card(3, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=4, game_nr=0, cards=[Card(0, 3), Card(0, 3), Card(2, 4), Card(3, 3)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=5, game_nr=0, cards=[Card(0, 1), Card(1, 3), Card(2, 3), Card(3, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=6, game_nr=0, cards=[Card(0, 1), Card(1, 0), Card(1, 2), Card(1, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=7, game_nr=0, cards=[Card(3, 2), Card(1, 0), Card(2, 1), Card(3, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        # fox caught
        Trick(nr=8, game_nr=0, cards=[Card(1, 3), Card(1, 1), Card(3, 0), Card(3, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        # karlchen
        Trick(nr=9, game_nr=0, cards=[Card(0, 4), Card(3, 2), Card(2, 4), Card(3, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
    ]
    for trick in tricks:
        sitting.evaluate_trick(trick, game_modus)

    sitting.evaluate_game(0, game_modus)

    assert sitting.points[0] == sitting.points[1] == -4
    assert sitting.points[2] == sitting.points[3] == 4
    assert len(sitting.extra_points) == 2
