"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from traiter.pylib.traits.pattern_compiler import Compiler

from ..part.pattern_compilers import PART_LABELS

CHILDREN = """
    color duration duration margin shape surface venation woodiness
    """.split()

PART_PARENTS = PART_LABELS + ["multiple_parts"]
PART_CHILDREN = CHILDREN + ["subpart"]
LINK_ONCE_CHILDREN = ["size", "count"]

SUBPART_PARENTS = ["subpart"]
SUBPART_CHILDREN = CHILDREN


DECODER = {
    "any": {},
    "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
}

LINK_PART = Compiler(
    label="link_part",
    decoder=DECODER
    | {
        "part": {"ENT_TYPE": {"IN": PART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": PART_CHILDREN}},
    },
    patterns=[
        "trait+ any* part+",
        "part+  any* trait+",
    ],
)

LINK_PART_ONCE = Compiler(
    label="link_part_once",
    decoder=DECODER
    | {
        "part": {"ENT_TYPE": {"IN": PART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LINK_ONCE_CHILDREN}},
    },
    patterns=[
        "trait+ any* part+",
        "part+  any* trait+",
    ],
)

LINK_SUBPART = Compiler(
    label="link_subpart",
    decoder=DECODER
    | {
        "subpart": {"ENT_TYPE": {"IN": SUBPART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": SUBPART_CHILDREN}},
    },
    patterns=[
        "trait+   clause* subpart+",
        "subpart+ clause* trait+",
    ],
)

LINK_SUBPART_ONCE = Compiler(
    label="link_subpart_once",
    decoder=DECODER
    | {
        "part": {"ENT_TYPE": {"IN": SUBPART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LINK_ONCE_CHILDREN}},
    },
    patterns=[
        "trait+ any* part+",
        "part+  any* trait+",
    ],
)
