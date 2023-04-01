from pathlib import Path

from traiter.pylib.traits.pattern_compiler import Compiler

from ..part import pattern_compilers as part

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / f"{TRAIT}.csv"

LOCATION_ENTS = """ location flower_location part_as_loc subpart_as_loc """.split()

DECODER = {
    "99-99": {"ENT_TYPE": "range"},
    "adj": {"POS": "ADJ"},
    "cm": {"ENT_TYPE": {"IN": ["metric_length", "imperial_length"]}},
    "joined": {"ENT_TYPE": "joined"},
    "leader": {"LOWER": {"IN": """to at embracing immersed from""".split()}},
    "location": {"ENT_TYPE": {"IN": LOCATION_ENTS}},
    "of": {"LOWER": "of"},
    "part": {"ENT_TYPE": {"IN": part.PART_LABELS}},
    "prep": {"POS": "ADP"},
    "subpart": {"ENT_TYPE": "subpart"},
}

COMPILERS = [
    Compiler(
        label="part_as_loc",
        decoder=DECODER,
        patterns=[
            "joined?  leader part",
            "location leader part",
            "leader prep part",
        ],
    ),
    Compiler(
        label="subpart_as_loc",
        decoder=DECODER,
        patterns=[
            "joined?  leader subpart",
            "joined?  leader subpart of adj? subpart",
            "location leader subpart",
            "location leader subpart of adj? subpart",
        ],
    ),
    Compiler(
        label="part_as_distance",
        decoder=DECODER,
        patterns=[
            "joined?  leader part prep? 99-99 cm",
            "location leader part prep? 99-99 cm",
        ],
    ),
]
