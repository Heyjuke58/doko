from dataclasses import dataclass

ANNOUCEMENT_STAGES = {
    0: 121,
    1: 151,
    2: 181,
    3: 211,
    4: 240,
}


@dataclass
class Announcement:
    stage: int
    team: int
