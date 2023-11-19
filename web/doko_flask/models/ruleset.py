from sqlalchemy.sql import func
from sqlalchemy_utils.types.choice import ChoiceType

from .. import db


class Ruleset(db.Model):
    __tablename__ = "rulesets"
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(
        db.DateTime(timezone=False), default=func.now(), nullable=False
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    tables = db.relationship("Table", backref="Ruleset")

    nines = db.Column(db.Boolean, nullable=False)
    DULLE_RULES = [
        ("first", "First dulle beats second"),
        ("second", "Second dulle beats first"),
    ]
    dulle_rule = db.Column(ChoiceType(DULLE_RULES), nullable=False)
    reverse_dulle_rule = db.Column(db.Boolean, nullable=False)
    ANNOUCMENT_COUNTING = [
        ("plus_2", "Announcement gives plus 2"),
        ("double", "Announcement doubles"),
    ]
    announcement_counting = db.Column(ChoiceType(ANNOUCMENT_COUNTING), nullable=False)
    also_double_extra_points = db.Column(db.Boolean, nullable=False)
    mandatory_announcement = db.Column(db.Boolean, nullable=False)
    piggies = db.Column(db.Boolean, nullable=False)
    piggies_auto_announce = db.Column(db.Boolean, nullable=False)
    piggies_in_poverty = db.Column(db.Boolean, nullable=False)
    piggies_in_trump_and_color_solo = db.Column(db.Boolean, nullable=False)

    ## Solos ##
    trump_solo = db.Column(db.Boolean, nullable=False)
    queens_solo = db.Column(db.Boolean, nullable=False)
    jacks_solo = db.Column(db.Boolean, nullable=False)
    fleshless_solo = db.Column(db.Boolean, nullable=False)
    queens_jacks_solo = db.Column(db.Boolean, nullable=False)
    kings_solo = db.Column(db.Boolean, nullable=False)
    COLOR_SOLOS = [
        ("diamonds_replaced", "Diamonds replaced Color Solo"),
        ("pure", "Pure Color Solo"),
        ("no", "No Color Solo"),
    ]
    color_solo = db.Column(ChoiceType(COLOR_SOLOS), nullable=False)

    ## Extra Points ##
    fox_caught = db.Column(db.Boolean, nullable=False)
    fox_caught_in_solos = db.Column(db.Boolean, nullable=False)
    fox_last_trick = db.Column(db.Boolean, nullable=False)
    doppelkopf = db.Column(db.Boolean, nullable=False)
    karlchen = db.Column(db.Boolean, nullable=False)
    KARLCHEN_CAUGHT = [
        ("any_card", "Karlchen caught with any card"),
        ("queen_of_diamonds", "Karlchen caught with Queen of Diamonds"),
        ("special", "Karlchen caught Special"),
        ("no", "No Karlchen caught"),
    ]
    karlchen_caught = db.Column(ChoiceType(KARLCHEN_CAUGHT), nullable=False)
    DULLE_CAUGHT = [
        ("any_card", "Dulle caught with any card"),
        ("dulle", "Dulle caught only with Dulle"),
        ("no", "No Dulle caught"),
    ]
    dulle_caught = db.Column(ChoiceType(DULLE_CAUGHT), nullable=False)
    jacks_pile = db.Column(db.Boolean, nullable=False)
    hearts_trick = db.Column(db.Boolean, nullable=False)

    ## Reservations ##
    poverty = db.Column(db.Boolean, nullable=False)
    WEDDING_DECISION_TRICK = [
        ("any_trick", "Any first Trick"),
        ("non_trump_trick", "First non-Trump Trick"),
        ("trump_trick", "First "),
        ("player_decides", "No Dulle caught"),
    ]
    wedding_decision_trick = db.Column(
        ChoiceType(WEDDING_DECISION_TRICK), nullable=False
    )
    five_louses = db.Column(db.Boolean, nullable=False)
    fox_highest_trump = db.Column(db.Boolean, nullable=False)
    seven_fulls = db.Column(db.Boolean, nullable=False)
    less_than_3_trumps = db.Column(db.Boolean, nullable=False)

    ## Bock ##
    BOCK_ROUND_SCHEME = [
        ("overlap", "Overlap Bock rounds"),
        ("append", "Append Bock rounds"),
    ]
    bock_round_scheme = db.Column(ChoiceType(BOCK_ROUND_SCHEME), nullable=False)
    hearts_trick_bock = db.Column(db.Boolean, nullable=False)
    split_arse_bock = db.Column(db.Boolean, nullable=False)
    lost_black_bock = db.Column(db.Boolean, nullable=False)
    both_announce_bock = db.Column(db.Boolean, nullable=False)
    jacks_pile_bock = db.Column(db.Boolean, nullable=False)

    def __init__(
        self,
        user_id,
        nines,
        dulle_rule,
        reverse_dulle_rule,
        announcement_counting,
        also_double_extra_points,
        mandatory_announcement,
        piggies,
        piggies_auto_announce,
        piggies_in_poverty,
        piggies_in_trump_and_color_solo,
        trump_solo,
        queens_solo,
        jacks_solo,
        fleshless_solo,
        queens_jacks_solo,
        kings_solo,
        color_solo,
        fox_caught,
        fox_caught_in_solos,
        fox_last_trick,
        doppelkopf,
        karlchen,
        karlchen_caught,
        dulle_caught,
        jacks_pile,
        hearts_trick,
        poverty,
        wedding_decision_trick,
        five_louses,
        fox_highest_trump,
        seven_fulls,
        less_than_3_trumps,
        bock_round_scheme,
        hearts_trick_bock,
        split_arse_bock,
        lost_black_bock,
        both_announce_bock,
        jacks_pile_bock,
    ):
        self.user_id = user_id

        self.nines = nines
        self.dulle_rule = dulle_rule
        self.reverse_dulle_rule = reverse_dulle_rule
        self.announcement_counting = announcement_counting
        self.also_double_extra_points = also_double_extra_points
        self.mandatory_announcement = mandatory_announcement
        self.piggies = piggies
        self.piggies_auto_announce = piggies_auto_announce
        self.piggies_in_poverty = piggies_in_poverty
        self.piggies_in_trump_and_color_solo = piggies_in_trump_and_color_solo
        self.trump_solo = trump_solo
        self.queens_solo = queens_solo
        self.jacks_solo = jacks_solo
        self.fleshless_solo = fleshless_solo
        self.queens_jacks_solo = queens_jacks_solo
        self.kings_solo = kings_solo
        self.color_solo = color_solo
        self.fox_caught = fox_caught
        self.fox_caught_in_solos = fox_caught_in_solos
        self.fox_last_trick = fox_last_trick
        self.doppelkopf = doppelkopf
        self.karlchen = karlchen
        self.karlchen_caught = karlchen_caught
        self.dulle_caught = dulle_caught
        self.jacks_pile = jacks_pile
        self.hearts_trick = hearts_trick
        self.poverty = poverty
        self.wedding_decision_trick = wedding_decision_trick
        self.five_louses = five_louses
        self.fox_highest_trump = fox_highest_trump
        self.seven_fulls = seven_fulls
        self.less_than_3_trumps = less_than_3_trumps
        self.bock_round_scheme = bock_round_scheme
        self.hearts_trick_bock = hearts_trick_bock
        self.split_arse_bock = split_arse_bock
        self.lost_black_bock = lost_black_bock
        self.both_announce_bock = both_announce_bock
        self.jacks_pile_bock = jacks_pile_bock
