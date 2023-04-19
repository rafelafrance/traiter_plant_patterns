from traiter.pylib import const as t_const
from traiter.pylib.traits.pattern_compiler import Compiler

from . import part_location_action as act
from plants.pylib.traits.part import part_action as p_act

LOCATION_ENTS = """
    location flower_location part_as_loc subpart_as_loc part_as_distance
    """.split()

TO = ["to"]


def part_location_patterns():
    decoder = {
        "9.9": {"TEXT": {"REGEX": t_const.FLOAT_TOKEN_RE}},
        "-/to": {"LOWER": {"IN": t_const.DASH + TO + ["_"]}},
        "adj": {"POS": "ADJ"},
        "cm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
        "joined": {"ENT_TYPE": "joined"},
        "leader": {"ENT_TYPE": "location_leader"},
        "location": {"ENT_TYPE": {"IN": LOCATION_ENTS}},
        "missing": {"ENT_TYPE": "missing"},
        "of": {"LOWER": "of"},
        "part": {"ENT_TYPE": {"IN": p_act.PART_LABELS}},
        "prep": {"POS": {"IN": ["ADP", "CCONJ"]}},
        "subpart": {"ENT_TYPE": "subpart"},
    }

    return [
        Compiler(
            label="part_as_loc",
            on_match=act.PART_LOCATION_MATCH,
            decoder=decoder,
            patterns=[
                "missing? joined?  leader prep? part",
                "missing? location leader       part",
                "                  leader       part prep? missing? joined",
            ],
        ),
        Compiler(
            label="subpart_as_loc",
            on_match=act.PART_LOCATION_MATCH,
            decoder=decoder,
            patterns=[
                "missing? joined?  leader subpart",
                "missing? joined?  leader subpart of adj? subpart",
                "missing? location leader subpart",
                "missing? location leader subpart of adj? subpart",
            ],
        ),
        Compiler(
            label="part_as_distance",
            on_match=act.PART_LOCATION_MATCH,
            decoder=decoder,
            patterns=[
                "missing? joined?  leader prep? part prep? 9.9 -/to* 9.9? cm",
                "missing? location leader prep? part prep? 9.9 -/to* 9.9? cm",
            ],
        ),
    ]
