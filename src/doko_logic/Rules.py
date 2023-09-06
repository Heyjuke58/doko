from typing import Tuple

from ExtraPoint import ExtraPoint
from GameModes import (
    COLOR_SOLO_DIAMONDS_REPLACED_GAME_MODES,
    NON_SOLO_GAME_MODES,
    SILENT_WEDDING_GAME_MODES,
    TRUMP_SOLO_GAME_MODES,
    ColorSoloDiamondsReplaced,
    ColorSoloDiamondsReplacedWithPiggies,
    GameModus,
    JacksSolo,
    KingsSolo,
    Meatless,
    Piggies,
    Poverty,
    PovertyWithPiggies,
    QueensJacksSolo,
    QueensSolo,
    Regular,
    SilentWedding,
    SilentWeddingWithPiggies,
    TrumpSolo,
    TrumpSoloWithPiggies,
    Wedding,
    WeddingWithPiggies,
)

EXTRA_POINTS = [
    ExtraPoint("doppelkopf", 1),
    ExtraPoint("fox_caught", 1),
    ExtraPoint("double_fox_caught", 2),
    ExtraPoint("fox_last_trick", 1),
    ExtraPoint("karlchen", 1),
    ExtraPoint("karlchen_caught", 1),
    ExtraPoint("karlchen_saved", 2),
    ExtraPoint("karlchen_save_denied", 3),
    ExtraPoint("dulle_caught_dulle", 1),
    ExtraPoint("jacks_pile", 1),
    ExtraPoint("hearts_trick_extra_point", 1),
]

# Rules class


class Rules:
    def __init__(
        self,
        ## DULLE ##
        dulle_1st_high: bool = False,  # False: 2nd high
        dulle_2nd_high_but_not_in_last_trick: bool = True,
        ## NINES ##
        nines: bool = False,
        ## PIGGIES ##
        piggies: bool = True,
        piggies_auto_announce: bool = True,
        ## SOLOS ##
        trump_solo: bool = True,
        color_solo_diamonds_replaced: bool = True,
        piggies_in_trump_and_color_solo: bool = True,
        color_solo_pure: bool = False,
        queens_solo: bool = True,
        jacks_solo: bool = True,
        queens_jacks_solo: bool = False,
        kings_solo: bool = True,
        meatless_solo: bool = True,
        ## EXTRAPOINTS ##
        fox_caught: bool = True,
        fox_caught_in_solos: bool = True,  # Trump or Diamonds replaced
        fox_last_trick: bool = False,
        doppelkopf: bool = True,
        dulle_caught_dulle: bool = False,
        karlchen: bool = True,
        karlchen_caught_any_card: bool = False,  # False: must be queen of diamonds
        karlchen_caught_plus: bool = True,  # Catch with diamonds queen, save with hearts queen, deny save with spades queen. The cards must match the teams. I.e. you get 2 point when you catch an jack of clubs from your partner that was trying to be caught with a queen of diamonds with
        jacks_pile: bool = True,  # TODO: explain
        hearts_trick_extra_point: bool = False,
        ## RESERVATIONS ##
        poverty: bool = True,
        five_louses: bool = False,
        fox_highest_trump: bool = True,
        wedding_1st_trick: bool = True,  # False: 1st non-trump trick
        ## COUNTING ##
        announcement_doubles: bool = False,  # False: 2 points
        announcement_doubles_also_extra_points: bool = False,
        ## ANNOUNCEMENTS ##
        before_own_2nd_card: bool = True,  # False: before 5th card
        ## BOCK ##
        append_bock_rounds: bool = False,  # False: overlap bock rounds
        hearts_trick_bock: bool = True,
        split_arse_bock: bool = True,
        lost_black_bock: bool = True,
        both_announce_bock: bool = True,
        jacks_pile_bock: bool = True,  # makes current game a bock game
    ) -> None:

        ## DULLE ##
        assert not (
            dulle_1st_high and dulle_2nd_high_but_not_in_last_trick
        ), "Cannot make 2nd dulle in last trick high when in the rest of the game it is not higher than 1st."
        self.dulle_1st_high = dulle_1st_high
        self.dulle_2nd_high_but_not_in_last_trick = dulle_2nd_high_but_not_in_last_trick if not dulle_1st_high else False

        ## NINES ##
        self.nines = nines

        ## PIGGIES ##
        assert not (not piggies and piggies_auto_announce), "Cannot auto announce piggies when they are not in the game."
        self.piggies = piggies
        self.piggies_auto_announce = piggies_auto_announce

        ## SOLOS ##
        self.trump_solo = trump_solo
        assert not (color_solo_diamonds_replaced and color_solo_pure), "Color solo has to either diamonds replaced or pure."
        assert not (not piggies and piggies_in_trump_and_color_solo), "Cannot have piggies in solos but not normally."
        self.color_solo_diamonds_replaced = color_solo_diamonds_replaced
        self.color_solo_pure = color_solo_pure
        self.piggies_in_trump_and_color_solo = piggies_in_trump_and_color_solo
        self.queens_solo = queens_solo
        self.jacks_solo = jacks_solo
        self.queens_jacks_solo = queens_jacks_solo
        self.kings_solo = kings_solo
        self.meatless_solo = meatless_solo

        ## EXTRAPOINTS ##
        self.fox_caught = fox_caught
        assert not (fox_caught_in_solos and not fox_caught), "Fox caught in solos but not real games, well.."
        self.fox_caught_in_solos = fox_caught_in_solos
        self.fox_last_trick = fox_last_trick
        self.doppelkopf = doppelkopf
        self.dulle_caught_dulle = dulle_caught_dulle
        self.karlchen = karlchen
        assert not (not karlchen and (karlchen_caught_any_card or karlchen_caught_plus)), "Cannot catch karlchen if it does not exist."
        self.karlchen_caught_any_card = karlchen_caught_any_card
        assert not (karlchen_caught_any_card and karlchen_caught_plus)
        self.karlchen_caught_plus = karlchen_caught_plus
        self.jacks_pile = jacks_pile
        assert not (hearts_trick_extra_point and nines), "Heart extra point with nines? Why though?!"
        self.hearts_trick_extra_point = hearts_trick_extra_point

        ## RESERVATIONS ##
        self.poverty = poverty
        self.five_louses = five_louses
        self.fox_highest_trump = fox_highest_trump
        self.wedding_1st_trick = wedding_1st_trick

        ## COUNTING ##
        self.announcement_doubles = announcement_doubles
        assert not (
            announcement_doubles_also_extra_points and not announcement_doubles
        ), "Extra points cannot be doubled when points are not doubled at all"
        self.announcement_doubles_also_extra_points = announcement_doubles_also_extra_points

        ## ANNOUNCEMENTS ##
        self.before_own_2nd_card = before_own_2nd_card

        ## BOCK ##
        self.append_bock_rounds = append_bock_rounds
        assert not (hearts_trick_bock and nines), "Hearts bock with nines? Why not though?"
        self.hearts_trick_bock = hearts_trick_bock
        self.split_arse_bock = split_arse_bock
        self.lost_black_bock = lost_black_bock
        self.both_announce_bock = both_announce_bock
        assert not (not jacks_pile and jacks_pile_bock)
        self.jacks_pile_bock = jacks_pile_bock

    # helper function to evaluate whether an extra point exists in a game modus and is activated by the rules
    def extra_point_possible(self, game_modus: GameModus, extra_point: str, last_trick: bool):
        if extra_point == "doppelkopf":
            return self.doppelkopf and isinstance(
                game_modus,
                tuple(NON_SOLO_GAME_MODES + SILENT_WEDDING_GAME_MODES + TRUMP_SOLO_GAME_MODES + COLOR_SOLO_DIAMONDS_REPLACED_GAME_MODES),
            )
        elif extra_point in {"fox_caught", "double_fox_caught"}:
            return self.fox_caught and (
                isinstance(game_modus, (Regular, Poverty, Wedding, SilentWedding))
                or (self.fox_caught_in_solos and isinstance(game_modus, (ColorSoloDiamondsReplaced, TrumpSolo)))
            )
        elif extra_point == "fox_last_trick":
            return (
                self.fox_last_trick
                and last_trick
                and (
                    isinstance(game_modus, (Regular, Poverty, Wedding, SilentWedding))
                    or (self.fox_caught_in_solos and isinstance(game_modus, (TrumpSolo, ColorSoloDiamondsReplaced)))
                )
            )
        # TODO: add rule if karlchen should exist in solo
        elif extra_point == "karlchen":
            return self.karlchen and isinstance(game_modus, tuple(NON_SOLO_GAME_MODES + SILENT_WEDDING_GAME_MODES)) and last_trick
        elif extra_point == "karlchen_caught":
            return (
                (self.karlchen_caught_any_card or self.karlchen_caught_plus)
                and isinstance(game_modus, tuple(NON_SOLO_GAME_MODES + SILENT_WEDDING_GAME_MODES))
                and last_trick
            )
        elif extra_point in {"karlchen_saved", "karlchen_save_denied"}:
            return self.karlchen_caught_plus and isinstance(game_modus, tuple(NON_SOLO_GAME_MODES + SILENT_WEDDING_GAME_MODES)) and last_trick
        elif extra_point == "dulle_caught_dulle":
            return self.dulle_caught_dulle and isinstance(game_modus, tuple(NON_SOLO_GAME_MODES + SILENT_WEDDING_GAME_MODES))
        elif extra_point == "jacks_pile":
            return self.jacks_pile and isinstance(game_modus, tuple(NON_SOLO_GAME_MODES + SILENT_WEDDING_GAME_MODES))
        elif extra_point == "hearts_trick_extra_point":
            return self.hearts_trick_extra_point and isinstance(game_modus, tuple(NON_SOLO_GAME_MODES + SILENT_WEDDING_GAME_MODES))
