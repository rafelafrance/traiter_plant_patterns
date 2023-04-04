from pathlib import Path

from traiter.pylib.traits.pattern_compiler import Compiler

from ..part import part_pattern_compilers as part

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / f"{TRAIT}.csv"

LOCATION_ENTS = """
    location flower_location part_as_loc subpart_as_loc part_as_distance
    """.split()

DECODER = {
    "99-99": {"ENT_TYPE": "range"},
    "adj": {"POS": "ADJ"},
    "cm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
    "joined": {"ENT_TYPE": "joined"},
    "leader": {"ENT_TYPE": "location_leader"},
    "location": {"ENT_TYPE": {"IN": LOCATION_ENTS}},
    "missing": {"ENT_TYPE": "missing"},
    "of": {"LOWER": "of"},
    "part": {"ENT_TYPE": {"IN": part.PART_LABELS}},
    "prep": {"POS": {"IN": ["ADP", "CCONJ"]}},
    "subpart": {"ENT_TYPE": "subpart"},
}

PART_LOCATION_COMPILERS = [
    Compiler(
        label="part_as_loc",
        decoder=DECODER,
        patterns=[
            "missing? joined?  leader prep? part",
            "missing? location leader       part",
            "                  leader       part prep? missing? joined",
        ],
    ),
    Compiler(
        label="subpart_as_loc",
        decoder=DECODER,
        patterns=[
            "missing? joined?  leader subpart",
            "missing? joined?  leader subpart of adj? subpart",
            "missing? location leader subpart",
            "missing? location leader subpart of adj? subpart",
        ],
    ),
    Compiler(
        label="part_as_distance",
        decoder=DECODER,
        patterns=[
            "missing? joined?  leader part prep? 99-99 cm",
            "missing? location leader part prep? 99-99 cm",
        ],
    ),
]
