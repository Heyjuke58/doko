from doko_logic import Card, Regular, Reservation, Rules, Trick

from .standard_setup import all_fine_hands, standard_test_setup, standard_test_setup_all_fine, wedding_hands


def test_fox_teams_clear():
    sitting = standard_test_setup()
    sitting.deal_cards(all_fine_hands)
    trick = Trick(nr=0, game_nr=0, cards=[Card(0, 3), Card(0, 3), Card(3, 0), Card(3, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1])
    sitting.evaluate_trick(trick, Regular())
    extra_point = sitting.extra_points[0]

    assert extra_point.name == "fox_caught", f"Extra point {extra_point.name} instead of fox_caught."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == 2
    assert extra_point.receiving_player == 0
    assert extra_point.team == 0
    assert extra_point.value == 1


def test_fox_teams_unclear():
    # wedding and first non trump trick decides
    sitting = standard_test_setup(rules=Rules(wedding_1st_trick=False))
    sitting.deal_cards(wedding_hands)
    reservations = [
        Reservation(value=1, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, _ = sitting.evaluate_reservations(reservations)
    sitting.teams = teams
    assert teams == [0, 2, 2, 2]
    trick = Trick(nr=0, game_nr=0, cards=[Card(1, 4), Card(0, 4), Card(3, 0), Card(3, 1)], players=[0, 1, 2, 3], teams=teams)
    sitting.evaluate_trick(trick, game_modus)
    extra_point = sitting.potential_extra_points[0]

    assert extra_point.name == "fox_caught", f"Extra point {extra_point.name} instead of fox_caught."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == 2
    assert extra_point.receiving_player == 1
    assert extra_point.team == 2
    assert extra_point.value == 1

    # the wedding is sealed with the next trick and the potential extra point should become a real one
    deciding_trick = Trick(nr=1, game_nr=0, cards=[Card(0, 2), Card(0, 1), Card(0, 1), Card(0, 2)], players=[0, 1, 2, 3], teams=teams)
    sitting.evaluate_trick(deciding_trick, game_modus)
    extra_point = sitting.extra_points[0]

    assert sitting.teams == [0, 0, 1, 1]
    assert extra_point.team == 0
    assert sitting.potential_extra_points == []


def test_fox_teams_unclear_one_caught_one_saved():
    # wedding and first non trump trick decides
    sitting = standard_test_setup(rules=Rules(wedding_1st_trick=False))
    sitting.deal_cards(wedding_hands)
    reservations = [
        Reservation(value=1, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, _ = sitting.evaluate_reservations(reservations)
    sitting.teams = teams
    assert teams == [0, 2, 2, 2]
    trick = Trick(nr=0, game_nr=0, cards=[Card(0, 4), Card(1, 4), Card(3, 0), Card(3, 0)], players=[0, 1, 2, 3], teams=teams)
    sitting.evaluate_trick(trick, game_modus)
    extra_point = sitting.potential_extra_points[0]

    assert extra_point.name == "double_fox_caught", f"Extra point {extra_point.name} instead of double_fox_caught."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == [2, 3]
    assert extra_point.receiving_player == 0
    assert extra_point.team == 0
    assert extra_point.value == 2

    # the wedding is sealed with the next trick and the potential extra point should become a real one
    deciding_trick = Trick(nr=1, game_nr=0, cards=[Card(0, 1), Card(0, 1), Card(0, 0), Card(0, 2)], players=[0, 1, 2, 3], teams=teams)
    sitting.evaluate_trick(deciding_trick, game_modus)
    extra_point = sitting.extra_points[0]

    assert sitting.teams == [0, 1, 0, 1]
    assert extra_point.team == 0
    assert extra_point.name == "fox_caught"
    assert extra_point.value == 1
    assert extra_point.paying_player == 3
    assert sitting.potential_extra_points == []


def test_doppelkopf_teams_clear():
    sitting = standard_test_setup()
    sitting.deal_cards(all_fine_hands)
    trick = Trick(nr=0, game_nr=0, cards=[Card(0, 0), Card(0, 0), Card(0, 1), Card(0, 1)], players=[0, 1, 2, 3], teams=[0, 0, 1, 1])
    sitting.evaluate_trick(trick, Regular())
    extra_point = sitting.extra_points[0]

    assert extra_point.name == "doppelkopf", f"Extra point {extra_point.name} instead of doppelkopf."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == None
    assert extra_point.receiving_player == 0
    assert extra_point.team == 0
    assert extra_point.value == 1


def test_doppelkopf_teams_unclear():
    sitting = standard_test_setup(rules=Rules(wedding_1st_trick=False))
    sitting.deal_cards(wedding_hands)
    reservations = [
        Reservation(value=1, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, _ = sitting.evaluate_reservations(reservations)
    sitting.teams = teams
    trick = Trick(nr=0, game_nr=0, cards=[Card(3, 1), Card(3, 1), Card(2, 1), Card(1, 0)], players=[0, 1, 2, 3], teams=teams)
    sitting.evaluate_trick(trick, game_modus)
    extra_point = sitting.potential_extra_points[0]

    assert extra_point.name == "doppelkopf", f"Extra point {extra_point.name} instead of doppelkopf."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == None
    assert extra_point.receiving_player == 2
    assert extra_point.team == 2
    assert extra_point.value == 1

    # the wedding is sealed with the next trick and the potential extra point should become a real one
    deciding_trick = Trick(nr=1, game_nr=0, cards=[Card(0, 1), Card(0, 1), Card(0, 0), Card(0, 2)], players=[0, 1, 2, 3], teams=teams)
    sitting.evaluate_trick(deciding_trick, game_modus)
    extra_point = sitting.extra_points[0]

    assert sitting.teams == [0, 1, 0, 1]
    assert extra_point.team == 0
    assert extra_point.name == "doppelkopf"
    assert extra_point.value == 1
    assert extra_point.paying_player == None
    assert sitting.potential_extra_points == []


def test_karlchen():
    sitting, game_modus = standard_test_setup_all_fine()
    trick = Trick(nr=9, game_nr=0, cards=[Card(0, 4), Card(0, 2), Card(0, 2), Card(2, 4)], players=[0, 1, 2, 3], teams=sitting.teams)
    sitting.evaluate_trick(trick, game_modus)
    extra_point = sitting.extra_points[0]

    assert extra_point.name == "karlchen", f"Extra point {extra_point.name} instead of karlchen."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == None
    assert extra_point.receiving_player == 0
    assert extra_point.team == 0
    assert extra_point.value == 1


def test_karlchen_caught_queen_of_diamonds():
    sitting, game_modus = standard_test_setup_all_fine()
    trick = Trick(nr=9, game_nr=0, cards=[Card(0, 4), Card(0, 2), Card(3, 3), Card(2, 4)], players=[0, 1, 2, 3], teams=sitting.teams)
    sitting.evaluate_trick(trick, game_modus)
    extra_point = sitting.extra_points[0]

    assert extra_point.name == "karlchen_caught", f"Extra point {extra_point.name} instead of karlchen_caught."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == None
    assert extra_point.receiving_player == 2
    assert extra_point.team == 1
    assert extra_point.value == 1


def test_karlchen_saved():
    sitting, game_modus = standard_test_setup_all_fine()
    trick = Trick(nr=9, game_nr=0, cards=[Card(0, 4), Card(2, 3), Card(3, 3), Card(2, 4)], players=[0, 1, 2, 3], teams=sitting.teams)
    sitting.evaluate_trick(trick, game_modus)
    extra_point = sitting.extra_points[0]

    assert extra_point.name == "karlchen_saved", f"Extra point {extra_point.name} instead of karlchen_saved."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == None
    assert extra_point.receiving_player == 1
    assert extra_point.team == 0
    assert extra_point.value == 2


def test_karlchen_saved_denied():
    sitting, game_modus = standard_test_setup_all_fine()
    trick = Trick(nr=9, game_nr=0, cards=[Card(0, 4), Card(2, 3), Card(3, 3), Card(1, 3)], players=[0, 1, 2, 3], teams=sitting.teams)
    sitting.evaluate_trick(trick, game_modus)
    extra_point = sitting.extra_points[0]

    assert extra_point.name == "karlchen_save_denied", f"Extra point {extra_point.name} instead of karlchen_save_denied."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == None
    assert extra_point.receiving_player == 3
    assert extra_point.team == 1
    assert extra_point.value == 3


def test_karlchen_caught_any_card():
    sitting, game_modus = standard_test_setup_all_fine(rules=Rules(karlchen_caught_any_card=True, karlchen_caught_plus=False))
    trick = Trick(nr=9, game_nr=0, cards=[Card(0, 4), Card(0, 2), Card(1, 3), Card(2, 4)], players=[0, 1, 2, 3], teams=sitting.teams)
    sitting.evaluate_trick(trick, game_modus)
    extra_point = sitting.extra_points[0]

    assert extra_point.name == "karlchen_caught", f"Extra point {extra_point.name} instead of karlchen_caught."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == None
    assert extra_point.receiving_player == 2
    assert extra_point.team == 1
    assert extra_point.value == 1


def test_karlchen_not_caught_since_same_team():
    sitting, game_modus = standard_test_setup_all_fine()
    trick = Trick(nr=9, game_nr=0, cards=[Card(0, 2), Card(0, 2), Card(0, 4), Card(3, 3)], players=[0, 1, 2, 3], teams=sitting.teams)
    sitting.evaluate_trick(trick, game_modus)
    assert sitting.extra_points == []


def test_karlchen_not_last_trick():
    sitting, game_modus = standard_test_setup_all_fine()
    trick = Trick(nr=8, game_nr=0, cards=[Card(0, 2), Card(0, 2), Card(0, 4), Card(0, 2)], players=[0, 1, 2, 3], teams=sitting.teams)
    sitting.evaluate_trick(trick, game_modus)
    assert sitting.extra_points == []


def test_jacks_pile():
    sitting, game_modus = standard_test_setup_all_fine()
    trick = Trick(nr=2, game_nr=0, cards=[Card(0, 4), Card(1, 4), Card(2, 4), Card(2, 4)], players=[0, 1, 2, 3], teams=sitting.teams)
    sitting.evaluate_trick(trick, game_modus)
    extra_point = sitting.extra_points[0]

    assert extra_point.name == "jacks_pile", f"Extra point {extra_point.name} instead of jacks_pile."
    assert extra_point.game_nr == 0
    assert extra_point.paying_player == None
    assert extra_point.receiving_player == 0
    assert extra_point.team == 0
    assert extra_point.value == 1
