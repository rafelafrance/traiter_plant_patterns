"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from traiter.pylib.matcher_compiler import Compiler

from ..part.part_compilers import PART_LABELS

SUBPART_PARENTS = ["subpart"]
SUBPART_CHILDREN = """ color joined shape margin surface venation """.split()

PART_PARENTS = PART_LABELS + ["subpart"]
PART_CHILDREN = SUBPART_CHILDREN + ["subpart"]
PART_ONCE_CHILDREN = ["size", "count"]

SUBPART_CHILDREN += PART_ONCE_CHILDREN

COMMON_DECODER = {
    "any": {},
    "clause": {"LOWER": {"REGEX": r"^([^.;:,]+)$"}},
    "phrase": {"LOWER": {"REGEX": r"^([^.;:]+)$"}},
}

LINK_PART = Compiler(
    "link_part",
    decoder=COMMON_DECODER
    | {
        "part": {"ENT_TYPE": {"IN": PART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": PART_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)

LINK_PART_ONCE = Compiler(
    "link_part_once",
    decoder=COMMON_DECODER
    | {
        "part": {"ENT_TYPE": {"IN": PART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": PART_ONCE_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)

LINK_SUBPART = Compiler(
    "link_subpart",
    decoder=COMMON_DECODER
    | {
        "subpart": {"ENT_TYPE": {"IN": SUBPART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": SUBPART_CHILDREN}},
    },
    patterns=[
        "trait   clause* subpart",
        "subpart clause* trait",
    ],
)

COMPILERS = [LINK_PART, LINK_PART_ONCE, LINK_SUBPART]
