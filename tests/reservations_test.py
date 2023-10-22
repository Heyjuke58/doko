from doko_logic import Card, ColorSoloDiamondsReplacedWithPiggies, Piggies, Regular, Reservation, SilentWedding, Solo, Wedding

from tests.standard_setup import all_fine_hands, standard_test_setup, wedding_hands

piggies_hands: list[list[Card]] = [
    [Card(0, 0), Card(0, 0), Card(0, 1), Card(0, 1), Card(0, 2), Card(0, 2), Card(1, 3), Card(0, 3), Card(0, 4), Card(0, 4)],
    [Card(1, 0), Card(1, 0), Card(1, 1), Card(1, 1), Card(1, 2), Card(1, 2), Card(1, 3), Card(0, 3), Card(1, 4), Card(1, 4)],
    [Card(2, 0), Card(2, 0), Card(2, 1), Card(2, 1), Card(2, 2), Card(2, 2), Card(2, 3), Card(2, 3), Card(2, 4), Card(2, 4)],
    [Card(3, 0), Card(3, 0), Card(3, 1), Card(3, 1), Card(3, 2), Card(3, 2), Card(3, 3), Card(3, 3), Card(3, 4), Card(3, 4)],
]

poverty_hands: list[list[Card]] = [
    [Card(0, 0), Card(0, 0), Card(0, 1), Card(0, 1), Card(0, 2), Card(0, 2), Card(1, 0), Card(0, 3), Card(0, 4), Card(0, 4)],
    [Card(1, 0), Card(1, 3), Card(1, 1), Card(1, 1), Card(1, 2), Card(1, 2), Card(1, 3), Card(0, 3), Card(1, 4), Card(1, 4)],
    [Card(3, 0), Card(2, 0), Card(2, 1), Card(2, 1), Card(2, 2), Card(2, 2), Card(2, 3), Card(2, 3), Card(2, 4), Card(2, 4)],
    [Card(3, 0), Card(2, 0), Card(3, 1), Card(3, 1), Card(3, 2), Card(3, 2), Card(3, 3), Card(3, 3), Card(3, 4), Card(3, 4)],
]

poverty_with_piggies_hands: list[list[Card]] = [
    [Card(0, 0), Card(0, 0), Card(0, 1), Card(0, 1), Card(0, 2), Card(0, 2), Card(1, 0), Card(0, 3), Card(0, 4), Card(0, 4)],
    [Card(1, 0), Card(1, 3), Card(1, 1), Card(1, 1), Card(1, 2), Card(1, 2), Card(1, 3), Card(0, 3), Card(1, 4), Card(1, 4)],
    [Card(2, 0), Card(2, 0), Card(2, 1), Card(2, 1), Card(2, 2), Card(2, 2), Card(2, 3), Card(2, 3), Card(2, 4), Card(2, 4)],
    [Card(3, 0), Card(3, 0), Card(3, 1), Card(3, 1), Card(3, 2), Card(3, 2), Card(3, 3), Card(3, 3), Card(3, 4), Card(3, 4)],
]


def test_all_fine():
    sitting = standard_test_setup()
    sitting.deal_cards(all_fine_hands)
    reservations = [
        Reservation(value=0, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, re_deal = sitting.evaluate_reservations(reservations)
    assert isinstance(game_modus, Regular), f"Game modus should be Regular when all fine not {game_modus}."
    assert teams == [0, 0, 1, 1], f"Teams should be [0, 0, 1, 1] not {teams}."
    assert not re_deal, f"All fine means no re-deal."


def test_wedding():
    sitting = standard_test_setup()
    sitting.deal_cards(wedding_hands)
    reservations = [
        Reservation(value=1, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, re_deal = sitting.evaluate_reservations(reservations)
    assert isinstance(game_modus, Wedding), f"Game modus should be Wedding not {game_modus}."
    assert teams == [0, 2, 2, 2], f"Teams should be [0, 2, 2, 2] not {teams}."
    assert not re_deal, f"Re-deal not False."


def test_piggies():
    sitting = standard_test_setup()
    sitting.deal_cards(piggies_hands)
    reservations = [
        Reservation(value=0, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3, play_piggies=True),
    ]
    game_modus, teams, re_deal = sitting.evaluate_reservations(reservations)
    assert isinstance(game_modus, Piggies), f"Game modus should be Piggies not {game_modus}."
    assert teams == [0, 0, 1, 1], f"Teams should be [0, 0, 1, 1] not {teams}."
    assert not re_deal, f"Re-deal not False."


def test_silent_wedding():
    sitting = standard_test_setup()
    sitting.deal_cards(wedding_hands)
    reservations = [
        Reservation(value=3, player=0, solo=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, re_deal = sitting.evaluate_reservations(reservations)  # add poverty handling for test
    assert isinstance(game_modus, SilentWedding), f"Game modus should be SilendWedding not {game_modus}."
    assert teams == [0, 1, 1, 1], f"Teams should be [0, 1, 1, 1] not {teams}."
    assert not re_deal, f"Re-deal not False."


def test_solo():
    sitting = standard_test_setup()
    reservations = [
        Reservation(value=3, player=0, solo=1),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, re_deal = sitting.evaluate_reservations(reservations)  # add poverty handling for test
    assert isinstance(game_modus, Solo), f"Game modus should be Solo not {game_modus}."
    assert teams == [0, 1, 1, 1], f"Teams should be [0, 1, 1, 1] not {teams}."
    assert not re_deal, f"Re-deal not False."


def test_color_solo_with_piggies():
    sitting = standard_test_setup()
    sitting.deal_cards(all_fine_hands)
    reservations = [
        Reservation(value=3, player=0, solo=2, color_solo_color=1),
        Reservation(value=4, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    game_modus, teams, re_deal = sitting.evaluate_reservations(reservations)  # add poverty handling for test
    assert isinstance(
        game_modus, ColorSoloDiamondsReplacedWithPiggies
    ), f"Game modus should be ColorSoloDiamondsReplacedWithPiggies not {game_modus}."
    assert teams == [0, 1, 1, 1], f"Teams should be [0, 1, 1, 1] not {teams}."
    assert not re_deal, f"Re-deal not False."


def test_throw():
    sitting = standard_test_setup()
    reservations = [
        Reservation(value=4, player=0),
        Reservation(value=0, player=1),
        Reservation(value=0, player=2),
        Reservation(value=0, player=3),
    ]
    _, __, re_deal = sitting.evaluate_reservations(reservations)  # add poverty handling for test
    assert re_deal, f"Throw means re-deal."


## TODO: implement handling of poverty in Test setting class

# def test_poverty():
#     sitting = standard_test_setup()
#     sitting.deal_cards(poverty_hands)
#     reservations = [
#         Reservation(value=2, player=0),
#         Reservation(value=0, player=1),
#         Reservation(value=0, player=2),
#         Reservation(value=0, player=3),
#     ]
#     with patch("sys.stdin", StringIO("FOO")), patch("sys.stdout", new_callable=StringIO) as mocked_out:
#         x = input()
#         print(x)

#         assert mocked_out.getvalue() == "FOO\n"
#     game_modus, teams, re_deal = sitting.evaluate_reservations(reservations)  # add poverty handling for test
#     assert isinstance(game_modus, Regular), f"Game modus should be Regular not {game_modus}."
#     assert teams == [0, 0, 1, 1], f"Teams should be [0, 0, 1, 1] not {teams}."
#     assert not re_deal, f"All fine means no re-deal."


# def test_poverty_with_piggies():
#     sitting = standard_test_setup()
#     sitting.deal_cards(piggies_hands)
#     reservations = [
#         Reservation(value=2, player=0),
#         Reservation(value=0, player=1),
#         Reservation(value=0, player=2),
#         Reservation(value=0, player=3),
#     ]
#     game_modus, teams, re_deal = sitting.evaluate_reservations(reservations)
#     assert isinstance(game_modus, Regular), f"Game modus should be Regular not {game_modus}."
#     assert teams == [0, 0, 1, 1], f"Teams should be [0, 0, 1, 1] not {teams}."
#     assert not re_deal, f"All fine means no re-deal."
