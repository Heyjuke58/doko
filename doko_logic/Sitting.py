import asyncio
import logging
import random
import socket
from functools import partial
from typing import Callable, Optional, Tuple, Union

import numpy as np
from aioconsole import ainput

from .Announcement import ANNOUCEMENT_STAGES, Announcement
from .Card import Card
from .Deck import Deck
from .ExtraPoint import (
    ExtraPoint,
    ExtraPointCheck,
    check_extra_point_doppelkopf,
    check_extra_point_dulle_caught_dulle,
    check_extra_point_fox_caught,
    check_extra_point_fox_last_trick,
    check_extra_point_foxes_caught,
    check_extra_point_hearts_trick,
    check_extra_point_jacks_pile,
    check_extra_point_karlchen,
    check_extra_point_karlchen_caught,
    check_extra_point_karlchen_save,
    check_extra_point_karlchen_save_denied,
)
from .GameModes import (
    NON_SOLO_GAME_MODES,
    SILENT_WEDDING_GAME_MODES,
    ColorSoloDiamondsReplaced,
    Fleshless,
    GameModus,
    JacksSolo,
    KingsSolo,
    Piggies,
    Poverty,
    PovertyWithPiggies,
    QueensJacksSolo,
    QueensSolo,
    Regular,
    SilentWedding,
    SilentWeddingWithPiggies,
    Solo,
    TrumpSolo,
    TrumpSoloWithPiggies,
    Wedding,
    WeddingWithPiggies,
)
from .Player import Player
from .Reservation import RESERVATION_VALUES, SOLO_VALUES, Reservation
from .Rules import EXTRA_POINTS, Rules
from .Trick import Trick

# Terminology
# Sitting: Overarching gathering of players to play n rounds of doppelkopf
# Round: 4 games (each player comes first in at least one of them by sitting order)
# Game: One time of dealing cards and playing them


class Sitting:
    def __init__(
        self,
        rules: Rules = Rules(),
        number_of_players: int = 4,
        player_names: list[str] = ["0", "1", "2", "3"],
        rounds: int = 5,
    ) -> None:
        self.rules = rules
        self.deck = Deck(self.rules.nines)
        self.number_of_players = number_of_players
        self.rounds = rounds
        assert len(player_names) == number_of_players, f"Invalid number of player names."
        self.players: list[Player] = [Player(nr=i, name=player_names[i]) for i in range(number_of_players)]
        self.points = {player.nr: 0 for player in self.players}

        self.extra_points: list[ExtraPoint] = []
        self.potential_extra_points: list[ExtraPoint] = []
        self.player_to_come_out = 0
        self.teams: list[int] = []  # 0: Re 1: Contra 2: Undecided || Order starts with player that came out the game
        self.cards_per_player: int = 10 if not self.rules.nines else 12
        self.announcements: dict[int, Announcement] = {}  # key is the player nr
        self.bock: list[int] = []  # game numbers that have bock. This list can hold numbers multiply times which means double/triple/... bock

    def play(self, hands: list[list[Card]] = []) -> None:
        for game_nr in range(self.rounds * self.number_of_players):
            # TODO: implement 5 player games

            self.player_to_come_out = game_nr % self.number_of_players
            self.teams = []

            game_modus = Regular()
            re_deal = True
            while re_deal:
                self.deal_cards(hands)
                self.print_reservation_help()
                reservations = []
                for i in range(4):
                    reservations.append(asyncio.run(self.await_reservation(self.players[(self.player_to_come_out + i) % 4])))

                game_modus, teams, re_deal = self.evaluate_reservations(reservations)
                self.teams = teams
                for i in range(4):
                    self.players[(self.player_to_come_out + i) % 4].set_team(self.teams[i])

            for player in self.players:
                player.final_hand_sort(game_modus, game_nr)

            self.announcements = {}

            tricks: dict[int, Trick] = {}
            for trick_nr in range(self.cards_per_player):
                tricks: dict[int, Trick] = {}
                cards: list[Card] = []
                players: list[int] = []
                for i in range(4):
                    cards.append(
                        asyncio.run(
                            self.await_card(
                                self.players[(self.player_to_come_out + i) % 4],
                                None if i == 0 else cards[0],
                                game_modus,
                            )
                        )
                    )
                    players.append((self.player_to_come_out + i) % 4)
                trick = Trick(trick_nr, game_nr, cards, players, self.teams)
                tricks[trick_nr] = trick
                self.evaluate_trick(trick, game_modus)

            self.evaluate_game(game_nr, game_modus)

    def deal_cards(self, hands: list[list[Card]]) -> None:
        """Randomly or purposely (for testing) deal cards

        Args:
            game_nr (int): Needed for testing puropses
            hands (list[list[Card]]): _description_
        """
        # every player gets a random hand
        if not hands:
            random.shuffle(self.deck.cards)
            for nr, player in enumerate(self.players):
                player.set_hand(self.deck.cards[nr * self.cards_per_player : (nr + 1) * self.cards_per_player])

        # deal fixed hands for testing purposes
        else:
            for nr, player in enumerate(self.players):
                player.set_hand(hands[nr])

    def make_announcement(self, player_nr: int, announcement: Announcement) -> None:
        # TODO: find a way to prevent a player to make ree/contra announcement after team mate has already done it.
        for k, v in self.announcements.items():
            if self.players[player_nr].team == announcement.team and k != player_nr:
                assert announcement.stage > v.stage, "Cannot make announcement under current team announcement!"
        if player_nr in self.announcements:
            assert self.announcements[player_nr].stage < announcement.stage, "Cannot make announcement under your current!"
        self.announcements[player_nr] = announcement

    @staticmethod
    def print_reservation_help():
        reservations = [f"{key}: {value}" for key, value in RESERVATION_VALUES.items()]
        print(f"Reservations:\n{reservations}")

    @staticmethod
    def print_solo_help():
        # TODO: adapt to existing solos in individual rules
        solos = [f"{key}: {value.__name__ if not isinstance(value, str) else value}" for key, value in SOLO_VALUES.items()]
        print(f"Possible Solos:\n{solos}")

    async def await_reservation(self, player: Player) -> Reservation:
        # reservation
        print(f"Hand of {player.name}\n{player.get_hand_str()}")
        legal_choice = False
        reservation = 0
        while not legal_choice:
            reservation = int(await ainput(f"{player.name} do you have any reservations?"))
            if reservation in {0, 1, 2, 3, 4}:
                legal_choice = True
            else:
                print("Not a legal choice!")

        # aks player whether piggies should be played
        play_piggies = False
        if player.has_piggies(trump_color=3) and self.rules.piggies:
            # TODO: decide which one to include!
            # play_piggies = bool(int(await ainput(f"{player.name} do you want to play foxes as piggies? {'Remember: You will auto-announce if you do.' if self.rules.piggies_auto_announce else ''}")))
            play_piggies = True

        # check whether palyer has wedding but announced fine
        if player.has_wedding():
            while reservation == 0:
                reservation = int(
                    await ainput(
                        f"Invalid choice of reservation. You have two queens of clubs. Either announce wedding, play a silent wedding or announce something else!"
                    )
                )
        # solo
        solo = None
        color_solo_color = None
        if reservation == 3:
            self.print_solo_help()
            solo = int(await ainput(f"{player.name} which solo do you want to play?"))
            if solo == 2:  # color solo
                color_solo_color = int(await ainput(f"{player.name} which color solo do you want to play? (0: clubs, 1: spades, 2: hearts)"))
                assert color_solo_color in {0, 1, 2}, "Invalid index for color solo!"

        return Reservation(value=reservation, player=player.nr, solo=solo, play_piggies=play_piggies, color_solo_color=color_solo_color)

    def evaluate_reservations(self, reservations: list[Reservation]) -> Tuple[GameModus, list[int], bool]:
        # TODO implement other ranking of reservations
        re_deal = False
        game_modus = Regular()
        teams = None

        def check_piggies(reservations: list[Reservation]):
            return any(reservation.play_piggies for reservation in reservations)

        # solo first
        for reservation in reservations:
            if reservation.is_solo():
                game_modus = reservation.get_solo(self.players, self.rules)
                teams = [0 if i == reservation.player else 1 for i in range(4)]
                self.set_teams(teams)
                return game_modus, teams, re_deal

        # throw
        for reservation in reservations:
            if reservation.is_throw():
                re_deal = True
                return game_modus, teams, re_deal  # type: ignore

        # poverty
        for reservation in reservations:
            if reservation.is_poverty():
                game_modus, teams, re_deal = asyncio.run(self.evaluate_poverty(reservation.player))
                self.set_teams(teams)
                return game_modus, teams, re_deal

        # wedding/silent wedding
        for reservation in reservations:
            if reservation.is_wedding():
                game_modus = Wedding() if not check_piggies(reservations) else WeddingWithPiggies()
                teams = [0 if i == reservation.player else 2 for i in range(4)]
                self.set_teams(teams)
                return game_modus, teams, re_deal
            if reservation.is_silent_wedding():
                game_modus = SilentWedding() if not check_piggies(reservations) else SilentWeddingWithPiggies()
                teams = [0 if i == reservation.player else 1 for i in range(4)]
                self.set_teams(teams)
                return game_modus, teams, re_deal

        # regular teams
        teams = [0 if self.players[(self.player_to_come_out + i) % 4].is_re() else 1 for i in range(4)]
        # piggies
        if check_piggies(reservations):
            game_modus = Piggies()

        self.set_teams(teams)

        return game_modus, teams, re_deal  # teams -> Re: 0, Contra: 1, To clarify (Wedding): 2

    async def evaluate_poverty(self, poor_player_idx: int) -> Tuple[GameModus, list[int], bool]:
        poor_player = self.players[poor_player_idx]
        trumps = [card for card in poor_player.hand if Regular().is_trump(card)]
        re_deal = True
        for i in range(3):
            accepting_player = self.players[(i + poor_player_idx + 1) % 4]
            accept_poverty = bool(
                int(
                    await ainput(
                        f"{accepting_player.name} do you want to take the {len(trumps)} trumps from player {poor_player.name}?\n{accepting_player.get_hand_str()}"
                    )
                )
            )
            if accept_poverty:
                teams = [0 if j == poor_player_idx or j == (i + poor_player_idx + 1) % 4 else 1 for j in range(4)]
                print(f"The trumps are: {[str(trump) for trump in trumps]}.")

                legal_action = False
                while not legal_action:
                    cards_idx_back = list(
                        map(
                            int,
                            await ainput(
                                f"{accepting_player.name} which cards should be returned? Format: x,y,z \nYour hand: {accepting_player.get_hand_str()}"
                            ).split(","),
                        )
                    )
                    legal_action = len(cards_idx_back) == len(trumps)
                    if not legal_action:
                        print(
                            f"Not a legal amount of cards returned. You attempted to return {len(cards_idx_back)} instead of {len(trumps)} cards. Try again!"
                        )

                cards_back = [accepting_player.hand[idx] for idx in cards_idx_back]
                print(f"{len([card for card in cards_back if Regular().is_trump(card)])} trumps back!")
                poor_player.handle_poverty(receiving_cards=cards_back, losing_cards=trumps)
                accepting_player.handle_poverty(receiving_cards=trumps, losing_cards=cards_back)
                re_deal = False
                break

        if any([player.has_piggies(trump_color=3) for player in self.players]):
            game_modus = PovertyWithPiggies()
        else:
            game_modus = Poverty()

        return game_modus, teams, re_deal

    async def await_card(self, player: Player, first_card: Union[None, Card], game_modus: GameModus) -> Card:
        while True:
            card_nr = int(await ainput(f"{player.name} which card do you play?\n{player.get_hand_str()}"))
            if not self.check_legality(player, player.hand[card_nr], first_card, game_modus):
                print("Your choice is not a legal card to play, choose another.")
            else:
                print(f"{str(player.hand[card_nr])} from {player.name}")
                break
        return player.play_card(card_nr)

    @staticmethod
    def check_legality(player: Player, card: Card, first_card: Union[None, Card], game_modus: GameModus) -> bool:
        if first_card is None:
            return True
        # non-trump
        if not game_modus.is_trump(first_card):
            trick_color = first_card.color
            if card.color == trick_color and not game_modus.is_trump(card):
                return True
            if game_modus.is_trump(card) or card.color != trick_color:
                for player_card in player.hand:
                    if player_card.color == trick_color and not game_modus.is_trump(player_card):
                        return False
                return True
        # trump
        else:
            if game_modus.is_trump(card):
                return True
            else:
                for player_card in player.hand:
                    if game_modus.is_trump(player_card):
                        return False
                return True

    def evaluate_trick(self, trick: Trick, game_modus: GameModus) -> None:
        trumps = [
            {"card": card, "card_idx": game_modus.trumps.index(card), "player": player}
            for player, card in zip(trick.players, trick.cards)
            if game_modus.is_trump(card)
        ]
        non_trumps = [
            {"card": card, "card_idx": card.symbol, "player": player}
            for player, card in zip(trick.players, trick.cards)
            if not game_modus.is_trump(card)
        ]

        def resolve_trick(
            self: Sitting, trick: Trick, challengers: list[dict], game_modus: GameModus, trump_trick: bool, reverse: bool = False
        ) -> None:
            idx = 0 if not reverse else -1  # decides whether second dulle catches first
            receiving_player: int = challengers[idx]["player"]
            trick.set_receiving_player(receiving_player)
            self.players[receiving_player].receive_trick(trick)

            # check if round modus is wedding and teams not yet evaluated
            if isinstance(game_modus, (Wedding, WeddingWithPiggies)) and any([2 == team for team in self.teams]):
                new_teams = None
                # check if another player than wedding player received trick
                if receiving_player != self.teams.index(0):
                    # check if wedding is settled
                    if self.rules.wedding_1st_trick or (not self.rules.wedding_1st_trick and not trump_trick):
                        new_teams = [0 if i == receiving_player else 1 for i in range(4) if self.teams[i] == 2]
                    # check if already third trick -> wedding player ends up alone
                    elif trick.nr >= 2:
                        new_teams = [1 for i in range(4) if self.teams[i] == 2]
                else:
                    # check if already third trick -> wedding player ends up alone
                    if trick.nr >= 2:
                        new_teams = [1 for i in range(4) if self.teams[i] == 2]
                if new_teams:
                    new_teams.insert(0, self.teams.index(0))  # add player that had wedding
                    self.set_teams(new_teams)
            self.check_hearts_trick_bock(trick, game_modus)

            self.check_extra_points(trick, game_modus)
            self.player_to_come_out = receiving_player
            print(f"{self.players[receiving_player].name} received the trick: {str(trick)}")

        # non-trump
        if not trumps:
            trick_color = trick.cards[0].color
            min_idx = min([non_trump["card_idx"] for non_trump in non_trumps if non_trump["card"].color == trick_color])
            challengers = [
                non_trump for non_trump in non_trumps if non_trump["card_idx"] == min_idx and non_trump["card"].color == trick_color
            ]
            resolve_trick(self, trick, challengers, game_modus, False)

        # trump
        else:
            min_idx = min([trump["card_idx"] for trump in trumps])
            challengers = [trump for trump in trumps if trump["card_idx"] == min_idx]
            if len(challengers) == 1:
                resolve_trick(self, trick, challengers, game_modus, True)
            else:
                if (
                    isinstance(game_modus, (Regular, Poverty, Wedding, SilentWedding, ColorSoloDiamondsReplaced))
                    and not self.rules.dulle_1st_high
                    and challengers[0]["card"].is_dulle()
                    and not (trick.nr + 1 == self.cards_per_player and self.rules.dulle_2nd_high_but_not_in_last_trick)
                ):
                    resolve_trick(
                        self, trick, challengers, game_modus, True, reverse=True
                    )  # since challengers are ordered and the second dulle beats the first dulle
                else:
                    resolve_trick(self, trick, challengers, game_modus, True)

    def check_hearts_trick_bock(self, trick: Trick, game_modus: GameModus):
        if isinstance(game_modus, tuple(NON_SOLO_GAME_MODES + SILENT_WEDDING_GAME_MODES)):
            hearts_ace = [x for x in trick.cards if x == Card(2, 0)]
            hearts_king = [x for x in trick.cards if x == Card(2, 2)]
            if len(hearts_ace) == 2 and len(hearts_king) == 2:
                if self.rules.hearts_trick_bock:
                    self.add_bock_games(trick.game_nr)

    def evaluate_game(self, game_nr: int, game_modus: GameModus) -> None:
        def add_extra_points(current_points: int):
            # TODO: winning team parameter needed?
            new_points = current_points
            for extra_point in self.extra_points:
                if extra_point.team == winning_team:
                    new_points += extra_point.value
                else:
                    new_points -= extra_point.value
            return new_points

        # determine card points
        re_card_points = 0
        contra_card_points = 0
        for player in self.players:
            if self.teams[player.nr] == 0:
                for key, value in player.card_points.items():
                    re_card_points += value
            else:
                for key, value in player.card_points.items():
                    contra_card_points += value
        # contra_card_points = 240 - re_card_points

        re_announcement = 120
        contra_announcement = 120
        # get new re/contra annoucnements
        for player_nr, announcement in self.announcements.items():
            new_announcement = ANNOUCEMENT_STAGES[announcement.stage]
            if self.teams[player_nr] == 0:
                re_announcement = new_announcement if new_announcement > re_announcement else re_announcement
            elif self.teams[player_nr] == 1:
                contra_announcement = new_announcement if new_announcement > contra_announcement else contra_announcement

        # determine the team who won the game also regarding announcements
        winning_team = 0 if re_announcement <= re_card_points and contra_announcement > contra_card_points else 1

        win_card_points = re_card_points if winning_team == 0 else contra_card_points

        win_announcement = re_announcement if winning_team == 0 else contra_announcement
        loose_announcement = contra_announcement if winning_team == 0 else re_announcement

        # for the win
        points = 1

        # if against party wins they get a bonus point
        if winning_team != 0:
            points += 1

        # Standard case (winning party has more than 120 points) but starting at 150 points, since contra can also win with 120 points
        for i in range(150, 241, 30):
            if win_card_points > i or win_card_points == 240:
                points += 1
                if win_announcement > i or win_announcement == 240 == win_card_points:
                    points += 1

        # Winning party has more than 120 and loosing party made wrong announcements
        for i in range(150, 241, 30):
            if win_card_points > 240 - i and loose_announcement > i:
                points += 2

        if self.rules.announcement_doubles_also_extra_points:
            points = add_extra_points(points)

        # get either 2 points for announcing the win or double points depending on the rules
        if win_announcement > 120:
            points = points * 2 if self.rules.announcement_doubles else points + 2

        if loose_announcement > 120:
            points = points * 2 if self.rules.announcement_doubles else points + 2

        if not self.rules.announcement_doubles_also_extra_points:
            points = add_extra_points(points)

        # check if jacks pile has happened
        if self.rules.jacks_pile_bock:
            jacks_piles = [x for x in self.extra_points if x.name == "jacks_pile"]
            for _ in jacks_piles:
                self.bock.append(game_nr)

        bock_count = self.bock.count(game_nr)
        points = points * bock_count if bock_count != 0 else points

        # evaluate bock
        if points == 0 and self.rules.split_arse_bock:
            self.add_bock_games(game_nr)
        if win_card_points == 240 and self.rules.lost_black_bock:
            self.add_bock_games(game_nr)
        if win_announcement > 120 and loose_announcement > 120 and self.rules.both_announce_bock:
            self.add_bock_games(game_nr)

        # points are distributed differently in solo rounds
        # TODO: points are stored redundant in sitting and player, decide which way to go later
        if isinstance(game_modus, Solo):
            for i in range(4):
                player = self.players[(self.player_to_come_out + i) % 4]
                if winning_team == player.team:
                    player.add_points(points * 3)
                    self.points[player.nr] += points * 3
                else:
                    player.add_points(-points)
                    self.points[player.nr] -= points
        else:
            for i in range(4):
                player = self.players[(self.player_to_come_out + i) % 4]
                if winning_team == player.team:
                    player.add_points(points)
                    self.points[player.nr] += points
                else:
                    player.add_points(-points)
                    self.points[player.nr] -= points

    def set_teams(self, new_teams: list[int]) -> None:
        self.teams = new_teams
        for player, team in zip(self.players, new_teams):
            player.set_team(team)
        self.evaluate_potential_extrapoints()

    def evaluate_potential_extrapoints(self) -> None:
        def add_extra_point(self: Sitting, extra_point: ExtraPoint, receiving_team: int):
            extra_point.team = receiving_team
            self.extra_points.append(extra_point)

        for extra_point in self.potential_extra_points:
            assert (
                type(extra_point.receiving_player) == int
            ), f"Error evaluating potential extra point {extra_point}: Could not determine new receiving team"
            new_receiving_team = self.teams[extra_point.receiving_player]
            if isinstance(extra_point.paying_player, list):
                new_paying_team = [self.teams[paying_player] for paying_player in extra_point.paying_player]
            else:
                new_paying_team = self.teams[extra_point.paying_player] if extra_point.paying_player else None

            # clear cases that are always extra points regardless of teams
            if extra_point.name in {"doppelkopf", "jacks_pile", "hearts_trick_extra_point"}:
                add_extra_point(self, extra_point, new_receiving_team)

            elif extra_point.name == "fox_caught":
                if new_receiving_team != new_paying_team:
                    add_extra_point(self, extra_point, new_receiving_team)

            elif extra_point.name == "double_fox_caught":
                assert isinstance(
                    new_paying_team, list
                ), f"Error evaluating potential extra point {extra_point}: Could not determine new receiving team "
                if all([team == new_paying_team[0] for team in new_paying_team]):
                    # in this case both foxes were caught
                    add_extra_point(self, extra_point, new_paying_team)  # type: ignore
                elif any([team == new_paying_team[0] for team in new_paying_team]):
                    # in this case only one fox was caught
                    extra_point.name = "fox_caught"
                    extra_point.value = 1
                    extra_point.paying_player = [player for player in extra_point.paying_player if self.teams[player] != new_receiving_team][
                        0
                    ]
                    add_extra_point(self, extra_point, new_receiving_team)

            elif extra_point.name == "dulle_caught_dulle":
                if new_receiving_team != new_paying_team:
                    add_extra_point(self, extra_point, new_receiving_team)

        # reset potential extra points for next game
        self.potential_extra_points = []

    def check_extra_point(self, trick: Trick, game_modus: GameModus, extra_point: str) -> ExtraPointCheck:
        """[summary]

        Args:
            trick (Trick): Trick to check
            game_modus (GameModus): Game modus
            extra_point (str): Which extra point should be checked

        Returns:
            Tuple[bool, int, int, int, bool]: point, receiving_team, receiving_player, paying_player, potential_extra_point
        """
        extra_point_checks: dict[str, Callable] = {
            "doppelkopf": partial(check_extra_point_doppelkopf, trick),
            "fox_caught": partial(check_extra_point_fox_caught, trick, game_modus),
            "double_fox_caught": partial(check_extra_point_foxes_caught, trick, game_modus),
            "dulle_caught_dulle": partial(check_extra_point_dulle_caught_dulle, trick),
            "hearts_trick_extra_point": partial(check_extra_point_hearts_trick, trick),
            "fox_last_trick": partial(check_extra_point_fox_last_trick, trick, game_modus),
            "karlchen": partial(check_extra_point_karlchen, trick),
            "karlchen_caught": partial(check_extra_point_karlchen_caught, trick, self.rules.karlchen_caught_any_card),
            "karlchen_saved": partial(check_extra_point_karlchen_save, trick),
            "karlchen_save_denied": partial(check_extra_point_karlchen_save_denied, trick),
            "jacks_pile": partial(check_extra_point_jacks_pile, trick),
        }
        return extra_point_checks[extra_point]()

    def check_extra_points(self, trick: Trick, game_modus: GameModus) -> None:
        for extra_point in EXTRA_POINTS:
            if self.rules.extra_point_possible(game_modus, extra_point.name, trick.nr + 1 == self.cards_per_player):
                point, receiving_team, receiving_player, paying_player, potential_extra_point = self.check_extra_point(
                    trick, game_modus, extra_point.name
                )
                if point:
                    # Teams not yet clear, could potentially be points at the end
                    if potential_extra_point:
                        self.potential_extra_points.append(
                            ExtraPoint(
                                extra_point.name, extra_point.value, receiving_team, receiving_player, paying_player, trick.nr, trick.game_nr
                            )
                        )
                    # Teams clear
                    else:
                        self.extra_points.append(
                            ExtraPoint(
                                extra_point.name, extra_point.value, receiving_team, receiving_player, paying_player, trick.nr, trick.game_nr
                            )
                        )

    def add_bock_games(self, game_nr: int) -> None:
        def extend_bock(index: int) -> None:
            self.bock.extend([i for i in range(index + 1, index + 1 + self.number_of_players)])

        if self.rules.append_bock_rounds:
            if not self.bock:
                extend_bock(game_nr)
            else:
                extend_bock(self.bock[-1])
        else:
            extend_bock(game_nr)
