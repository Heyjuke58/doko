from dataclasses import dataclass
from typing import Optional, Tuple, Union

from Card import Card
from GameModes import ColorSoloDiamondsReplaced, GameModus
from Trick import Trick

PayingPlayer = Optional[Union[int, list[int]]]

ExtraPointCheck = Tuple[bool, int, int, PayingPlayer, bool]  # point, receiving_team, receiving_player, paying_player, potential_extra_point


@dataclass
class ExtraPoint:
    name: str
    value: int
    team: Optional[int] = None
    receiving_player: Optional[int] = None
    paying_player: PayingPlayer = None
    trick_nr: Optional[int] = None
    game_nr: Optional[int] = None


## HELPER FUNCTIONS


def check_extra_point_standard_positive_return(trick: Trick) -> ExtraPointCheck:
    return (
        True,
        trick.teams[trick.receiving_player],
        trick.receiving_player,
        None,
        any([team == 2 for team in trick.teams]) if trick.teams[trick.receiving_player] == 2 else False,
    )


def check_extra_point_standard_positive_return_teams_decided(trick: Trick) -> ExtraPointCheck:
    return (
        True,
        trick.teams[trick.receiving_player],
        trick.receiving_player,
        None,
        any([team == 2 for team in trick.teams]),
    )


def check_extra_point_standard_negative_return() -> ExtraPointCheck:
    return False, -1, -1, None, False


def get_foxes(trick: Trick, game_modus) -> list[int]:
    foxes: list[int] = []
    # check which color is trump
    if isinstance(game_modus, ColorSoloDiamondsReplaced):
        # second index is losing_player
        foxes = [trick.players[i] for i, card in enumerate(trick.cards) if card == Card(game_modus.color, 0)]
    else:
        foxes = [trick.players[i] for i, card in enumerate(trick.cards) if card == Card(3, 0)]

    return foxes


def get_caught_foxes(trick: Trick, foxes: list[int], receiving_team: int) -> list[int]:
    fox_from_player: list[int] = []  # list of foxes that went to the opposing team
    for paying_player in foxes:
        if receiving_team != trick.teams[paying_player] or (receiving_team == 2 == trick.teams[paying_player]):
            fox_from_player.append(paying_player)
    return fox_from_player


def get_specific_cards(trick: Trick, color: int, symbol: int) -> list[int]:
    return [player for card, player in zip(trick.cards, trick.players) if card == Card(color=color, symbol=symbol)]


## EXTRA POINT CHECK FUNTIONS


def check_extra_point_doppelkopf(trick: Trick) -> ExtraPointCheck:
    if all([card.get_value() >= 10 for card in trick.cards]):
        return check_extra_point_standard_positive_return(trick)
    return check_extra_point_standard_negative_return()


def check_extra_point_fox_caught(trick: Trick, game_modus: GameModus) -> ExtraPointCheck:
    foxes = get_foxes(trick, game_modus)  # get all foxes in trick
    receiving_team = trick.teams[trick.receiving_player]
    potential_extra_point = any([team == 2 for team in trick.teams])

    # case there is only one fox
    if len(foxes) == 1:
        paying_player = foxes[0]
        if receiving_team != trick.teams[paying_player] or (receiving_team == 2 == trick.teams[paying_player]):
            return True, receiving_team, trick.receiving_player, paying_player, potential_extra_point
    # case there are two foxes
    elif len(foxes) == 2:
        fox_from_player = get_caught_foxes(trick, foxes, receiving_team)  # list of foxes that went to the opposing team
        for paying_player in foxes:
            if receiving_team != trick.teams[paying_player] or (receiving_team == 2 == trick.teams[paying_player]):
                fox_from_player.append(paying_player)
        # case when one fox is caught and the other saved
        if len(fox_from_player) == 1:
            return True, receiving_team, trick.receiving_player, fox_from_player[0], potential_extra_point
    return check_extra_point_standard_negative_return()


def check_extra_point_foxes_caught(trick: Trick, game_modus: GameModus) -> ExtraPointCheck:
    foxes = get_foxes(trick, game_modus)  # get all foxes in trick
    receiving_team = trick.teams[trick.receiving_player]

    # case there are two foxes
    if len(foxes) == 2:
        fox_from_player = get_caught_foxes(trick, foxes, receiving_team)  # list of foxes that went to the opposing team
        # case when two foxes were caught
        if len(fox_from_player) == 2:
            return True, receiving_team, trick.receiving_player, fox_from_player, any([team == 2 for team in trick.teams])
    return check_extra_point_standard_negative_return()


def check_extra_point_fox_last_trick(trick: Trick, game_modus: GameModus) -> ExtraPointCheck:
    foxes = get_foxes(trick, game_modus)
    for player in foxes:
        if trick.receiving_player == player:
            return check_extra_point_standard_positive_return_teams_decided(trick)
    return check_extra_point_standard_negative_return()


def check_extra_point_hearts_trick(trick: Trick) -> ExtraPointCheck:
    # should be disabled in a game with 9's
    if len([card for card in trick.cards if (card == Card(color=3, symbol=0) or card == Card(color=3, symbol=2))]) == 4:
        return check_extra_point_standard_positive_return(trick)
    return check_extra_point_standard_negative_return()


def check_extra_point_jacks_pile(trick: Trick) -> ExtraPointCheck:
    if all([card.symbol == 4 for card in trick.cards]):
        return check_extra_point_standard_positive_return(trick)
    return check_extra_point_standard_negative_return()


def check_extra_point_dulle_caught_dulle(trick: Trick) -> ExtraPointCheck:
    paying_player = [player for card, player in zip(trick.cards, trick.players) if card.is_dulle() and player != trick.receiving_player]
    benefitting_player = [player for card, player in zip(trick.cards, trick.players) if card.is_dulle() and player == trick.receiving_player]
    if len(paying_player) == 1 and len(benefitting_player) == 1:
        if (trick.teams[paying_player[0]] != trick.teams[benefitting_player[0]]) or (
            trick.teams[paying_player[0]] == 2 == trick.teams[benefitting_player[0]]
        ):
            return (
                True,
                trick.teams[trick.receiving_player],
                trick.receiving_player,
                paying_player[0],
                any([team == 2 for team in trick.teams]),
            )
    return check_extra_point_standard_negative_return()


def check_extra_point_karlchen(trick: Trick) -> ExtraPointCheck:
    players_playing_jacks_of_clubs = get_specific_cards(trick, color=0, symbol=4)
    for player in players_playing_jacks_of_clubs:
        if trick.receiving_player == player:
            return check_extra_point_standard_positive_return_teams_decided(trick)
    return check_extra_point_standard_negative_return()


def check_extra_point_karlchen_caught(trick: Trick, rule_any_card: bool = False) -> ExtraPointCheck:
    players_playing_jacks_of_clubs = get_specific_cards(trick, color=0, symbol=4)
    if rule_any_card:
        for paying_player in players_playing_jacks_of_clubs:
            if trick.teams[trick.receiving_player] != trick.teams[paying_player]:
                return check_extra_point_standard_positive_return_teams_decided(trick)
    else:
        players_playing_queens_of_diamonds = get_specific_cards(trick, color=3, symbol=3)
        if any([trick.receiving_player == player for player in players_playing_queens_of_diamonds]):
            for paying_player in players_playing_jacks_of_clubs:
                if trick.teams[trick.receiving_player] != trick.teams[paying_player]:
                    return check_extra_point_standard_positive_return_teams_decided(trick)
    return check_extra_point_standard_negative_return()


def check_extra_point_karlchen_save(trick: Trick) -> ExtraPointCheck:
    players_playing_queens_of_hearts = get_specific_cards(trick, color=2, symbol=3)
    if any([trick.receiving_player == player for player in players_playing_queens_of_hearts]):
        players_playing_queens_of_diamonds = get_specific_cards(trick, color=3, symbol=3)
        if any([trick.teams[player] != trick.teams[trick.receiving_player] for player in players_playing_queens_of_diamonds]):
            players_playing_jacks_of_clubs = get_specific_cards(trick, color=0, symbol=4)
            if any([trick.teams[player] == trick.teams[trick.receiving_player] for player in players_playing_jacks_of_clubs]):
                return check_extra_point_standard_positive_return_teams_decided(trick)
    return check_extra_point_standard_negative_return()


def check_extra_point_karlchen_save_denied(trick: Trick) -> ExtraPointCheck:
    players_playing_queens_of_spades = get_specific_cards(trick, color=1, symbol=3)
    if any([trick.receiving_player == player for player in players_playing_queens_of_spades]):
        players_playing_queens_of_hearts = get_specific_cards(trick, color=2, symbol=3)
        if any([trick.receiving_player != player for player in players_playing_queens_of_hearts]):
            players_playing_queens_of_diamonds = get_specific_cards(trick, color=3, symbol=3)
            if any([trick.teams[player] == trick.teams[trick.receiving_player] for player in players_playing_queens_of_diamonds]):
                players_playing_jacks_of_clubs = get_specific_cards(trick, color=0, symbol=4)
                if any([trick.teams[player] != trick.teams[trick.receiving_player] for player in players_playing_jacks_of_clubs]):
                    return check_extra_point_standard_positive_return_teams_decided(trick)
    return check_extra_point_standard_negative_return()
