from pathlib import Path

from traiter.pylib import const as t_const
from traiter.pylib import trait_util
from traiter.pylib.matcher_compiler import Compiler

from ..part import part_compilers as part

HERE = Path(__file__).parent
TRAIT = HERE.stem

CSV = HERE / f"{TRAIT}.csv"

LOCATION_ENTS = """ location flower_location part_as_loc subpart_as_loc """.split()

DECODER = {
    "adj": {"POS": "ADJ"},
    "cm": {"ENT_TYPE": "metric_length"},
    "joined": {"ENT_TYPE": "joined"},
    "leader": {"LOWER": {"IN": """to at embracing immersed from""".split()}},
    "location": {"ENT_TYPE": {"IN": LOCATION_ENTS}},
    "of": {"LOWER": "of"},
    "part": {"ENT_TYPE": {"IN": part.PART_LABELS}},
    "prep": {"POS": "ADP"},
    "sex": {"ENT_TYPE": "sex"},
    "subpart": {"ENT_TYPE": "subpart"},
}

PART_AS_LOCATION = Compiler(
    "part_as_loc",
    decoder=DECODER,
    patterns=[
        "joined?  leader part",
        "location leader part",
        "leader prep part",
    ],
)

SUBPART_AS_LOCATION = Compiler(
    "subpart_as_loc",
    decoder=DECODER,
    patterns=[
        "joined?  leader subpart",
        "joined?  leader subpart of adj? subpart",
        "location leader subpart",
        "location leader subpart of adj? subpart",
    ],
)

PART_AS_DISTANCE = Compiler(
    "part_as_distance",
    decoder=DECODER,
    patterns=[
        "joined?  leader part prep? 99-99 cm",
        "location leader part prep? 99-99 cm",
    ],
)
