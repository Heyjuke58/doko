from doko_logic import Announcement, Card, Regular, Reservation, Trick
from tests.standard_setup import all_fine_hands, standard_test_setup, standard_test_setup_all_fine, wedding_hands

all_fine_hands: list[list[Card]] = [
    [Card(0, 0), Card(0, 0), Card(0, 1), Card(0, 1), Card(2, 2), Card(3, 2), Card(1, 3), Card(0, 3), Card(0, 4), Card(0, 4)],
    [Card(1, 0), Card(1, 0), Card(1, 1), Card(1, 1), Card(2, 2), Card(3, 2), Card(1, 3), Card(0, 3), Card(1, 4), Card(1, 4)],
    [Card(3, 0), Card(2, 0), Card(2, 1), Card(2, 1), Card(0, 2), Card(1, 2), Card(2, 3), Card(2, 3), Card(2, 4), Card(2, 4)],
    [Card(3, 0), Card(2, 0), Card(3, 1), Card(3, 1), Card(0, 2), Card(1, 2), Card(3, 3), Card(3, 3), Card(3, 4), Card(3, 4)],
]
black_hands_re: list[list[Card]] = [
    [Card(0, 3), Card(1, 3), Card(1, 3), Card(2, 3), Card(2, 3), Card(3, 3), Card(3, 3), Card(2, 1), Card(2, 1), Card(3, 0)],
    [Card(0, 3), Card(1, 4), Card(1, 4), Card(2, 4), Card(2, 4), Card(3, 4), Card(3, 4), Card(0, 4), Card(0, 4), Card(3, 0)],
    [Card(0, 0), Card(0, 0), Card(0, 1), Card(0, 1), Card(0, 2), Card(0, 2), Card(2, 0), Card(2, 0), Card(2, 2), Card(2, 2)],
    [Card(1, 0), Card(1, 0), Card(1, 1), Card(1, 1), Card(1, 2), Card(1, 2), Card(3, 2), Card(3, 2), Card(3, 1), Card(3, 1)],
]
black_hands_contra: list[list[Card]] = [
    [Card(0, 3), Card(0, 0), Card(0, 1), Card(0, 1), Card(0, 2), Card(0, 2), Card(2, 0), Card(2, 0), Card(2, 2), Card(2, 2)],
    [Card(0, 3), Card(1, 0), Card(1, 1), Card(1, 1), Card(1, 2), Card(1, 2), Card(3, 2), Card(3, 2), Card(3, 1), Card(3, 1)],
    [Card(0, 0), Card(1, 3), Card(1, 3), Card(2, 3), Card(2, 3), Card(3, 3), Card(3, 3), Card(2, 1), Card(2, 1), Card(3, 0)],
    [Card(1, 0), Card(1, 4), Card(1, 4), Card(2, 4), Card(2, 4), Card(3, 4), Card(3, 4), Card(0, 4), Card(0, 4), Card(3, 0)],
]
queen_solo_hands: list[list[Card]] = [
    [Card(0, 3), Card(0, 3), Card(1, 3), Card(1, 3), Card(2, 3), Card(2, 3), Card(3, 3), Card(3, 3), Card(1, 0), Card(0, 0)],
    [Card(2, 1), Card(1, 4), Card(1, 4), Card(2, 4), Card(2, 4), Card(3, 4), Card(3, 4), Card(0, 4), Card(0, 4), Card(0, 1)],
    [Card(2, 1), Card(2, 2), Card(3, 1), Card(3, 1), Card(3, 0), Card(3, 0), Card(3, 2), Card(3, 2), Card(2, 2), Card(0, 1)],
    [Card(1, 0), Card(0, 2), Card(1, 1), Card(1, 1), Card(1, 2), Card(1, 2), Card(2, 0), Card(2, 0), Card(0, 2), Card(0, 0)],
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
    # re party announces no 90 but contra party gets over 90 points
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


def test_re_win_black():
    sitting = standard_test_setup()
    sitting.deal_cards(black_hands_re)
    reservations = [
        Reservation(value=0, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, _ = sitting.evaluate_reservations(reservations)
    # re party wins black
    tricks = [
        Trick(nr=0, game_nr=0, cards=[Card(2, 1), Card(3, 0), Card(2, 2), Card(3, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=1, game_nr=0, cards=[Card(0, 3), Card(3, 4), Card(2, 2), Card(3, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=2, game_nr=0, cards=[Card(1, 3), Card(3, 4), Card(2, 0), Card(3, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=3, game_nr=0, cards=[Card(1, 3), Card(2, 4), Card(2, 0), Card(3, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=4, game_nr=0, cards=[Card(2, 3), Card(2, 4), Card(0, 0), Card(1, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=5, game_nr=0, cards=[Card(2, 3), Card(1, 4), Card(0, 0), Card(1, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=6, game_nr=0, cards=[Card(3, 3), Card(1, 4), Card(0, 1), Card(1, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=7, game_nr=0, cards=[Card(3, 3), Card(0, 4), Card(0, 1), Card(1, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=8, game_nr=0, cards=[Card(3, 0), Card(0, 4), Card(0, 2), Card(1, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=9, game_nr=0, cards=[Card(2, 1), Card(0, 3), Card(0, 2), Card(1, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
    ]
    for trick in tricks:
        sitting.evaluate_trick(trick, game_modus)

    sitting.evaluate_game(0, game_modus)

    assert sitting.points[0] == sitting.points[1] == 5
    assert sitting.points[2] == sitting.points[3] == -5
    assert sitting.extra_points == []


def test_re_win_black_announced():
    sitting = standard_test_setup()
    sitting.deal_cards(black_hands_re)
    reservations = [
        Reservation(value=0, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, _ = sitting.evaluate_reservations(reservations)
    sitting.make_announcement(player_nr=0, announcement=Announcement(stage=4, team=0))
    # re party wins black
    tricks = [
        Trick(nr=0, game_nr=0, cards=[Card(2, 1), Card(3, 0), Card(2, 2), Card(3, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=1, game_nr=0, cards=[Card(0, 3), Card(3, 4), Card(2, 2), Card(3, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=2, game_nr=0, cards=[Card(1, 3), Card(3, 4), Card(2, 0), Card(3, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=3, game_nr=0, cards=[Card(1, 3), Card(2, 4), Card(2, 0), Card(3, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=4, game_nr=0, cards=[Card(2, 3), Card(2, 4), Card(0, 0), Card(1, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=5, game_nr=0, cards=[Card(2, 3), Card(1, 4), Card(0, 0), Card(1, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=6, game_nr=0, cards=[Card(3, 3), Card(1, 4), Card(0, 1), Card(1, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=7, game_nr=0, cards=[Card(3, 3), Card(0, 4), Card(0, 1), Card(1, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=8, game_nr=0, cards=[Card(3, 0), Card(0, 4), Card(0, 2), Card(1, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=9, game_nr=0, cards=[Card(2, 1), Card(0, 3), Card(0, 2), Card(1, 2)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
    ]
    for trick in tricks:
        sitting.evaluate_trick(trick, game_modus)

    sitting.evaluate_game(0, game_modus)

    assert sitting.points[0] == sitting.points[1] == 11
    assert sitting.points[2] == sitting.points[3] == -11
    assert sitting.extra_points == []
    assert sitting.bock == [1, 2, 3, 4]


def test_contra_win_black_announced():
    sitting = standard_test_setup()
    sitting.deal_cards(black_hands_contra)
    reservations = [
        Reservation(value=0, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, _ = sitting.evaluate_reservations(reservations)
    sitting.make_announcement(player_nr=2, announcement=Announcement(stage=4, team=0))
    # re party wins black
    tricks = [
        Trick(nr=0, game_nr=0, cards=[Card(0, 3), Card(0, 3), Card(2, 1), Card(3, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=1, game_nr=0, cards=[Card(2, 2), Card(3, 1), Card(0, 0), Card(3, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=2, game_nr=0, cards=[Card(3, 2), Card(2, 2), Card(1, 3), Card(3, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=3, game_nr=0, cards=[Card(2, 0), Card(3, 2), Card(1, 3), Card(2, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=4, game_nr=0, cards=[Card(2, 0), Card(3, 1), Card(2, 3), Card(2, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=5, game_nr=0, cards=[Card(0, 0), Card(1, 0), Card(2, 3), Card(1, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=6, game_nr=0, cards=[Card(0, 1), Card(1, 1), Card(3, 3), Card(1, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=7, game_nr=0, cards=[Card(0, 1), Card(1, 1), Card(3, 3), Card(0, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=8, game_nr=0, cards=[Card(0, 2), Card(1, 2), Card(3, 0), Card(0, 4)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
        Trick(nr=9, game_nr=0, cards=[Card(0, 2), Card(1, 2), Card(2, 1), Card(1, 0)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1]),
    ]
    for trick in tricks:
        sitting.evaluate_trick(trick, game_modus)

    sitting.evaluate_game(0, game_modus)

    assert sitting.points[2] == sitting.points[3] == 12
    assert sitting.points[0] == sitting.points[1] == -12
    assert sitting.extra_points == []
    assert sitting.bock == [1, 2, 3, 4]


def test_solo_win_black_announced():
    sitting = standard_test_setup()
    sitting.deal_cards(queen_solo_hands)
    reservations = [
        Reservation(value=3, player=0, solo=3),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, _ = sitting.evaluate_reservations(reservations)
    sitting.make_announcement(player_nr=0, announcement=Announcement(stage=4, team=0))
    # re party wins black
    tricks = [
        # no doppelkopf since solo
        Trick(nr=0, game_nr=0, cards=[Card(0, 0), Card(0, 1), Card(0, 1), Card(0, 0)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
        Trick(nr=1, game_nr=0, cards=[Card(1, 0), Card(3, 4), Card(2, 2), Card(0, 2)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
        Trick(nr=2, game_nr=0, cards=[Card(0, 3), Card(3, 4), Card(2, 2), Card(0, 2)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
        Trick(nr=3, game_nr=0, cards=[Card(0, 3), Card(2, 4), Card(3, 0), Card(2, 0)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
        Trick(nr=4, game_nr=0, cards=[Card(1, 3), Card(2, 4), Card(3, 0), Card(2, 0)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
        Trick(nr=5, game_nr=0, cards=[Card(1, 3), Card(1, 4), Card(3, 1), Card(1, 0)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
        Trick(nr=6, game_nr=0, cards=[Card(2, 3), Card(1, 4), Card(3, 1), Card(1, 1)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
        Trick(nr=7, game_nr=0, cards=[Card(2, 3), Card(0, 4), Card(3, 2), Card(1, 1)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
        Trick(nr=8, game_nr=0, cards=[Card(3, 3), Card(0, 4), Card(3, 2), Card(1, 2)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
        Trick(nr=9, game_nr=0, cards=[Card(3, 3), Card(2, 1), Card(2, 1), Card(1, 2)], players=[0, 1, 2, 3], teams=[0, 1, 1, 1]),
    ]
    for trick in tricks:
        sitting.evaluate_trick(trick, game_modus)

    sitting.evaluate_game(0, game_modus)

    assert sitting.points[0] == 33
    assert sitting.points[1] == sitting.points[2] == sitting.points[3] == -11
    assert sitting.extra_points == []
    assert sitting.bock == [1, 2, 3, 4]
