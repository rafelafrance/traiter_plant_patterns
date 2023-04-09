"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from traiter.pylib.traits.pattern_compiler import Compiler

from ..part.part_patterns import PART_LABELS

CHILDREN = """
    color duration duration margin shape surface venation woodiness
    """.split()

LINK_PART_PARENTS = PART_LABELS + ["multiple_parts"]
LINK_PART_CHILDREN = CHILDREN + ["subpart"]
LINK_PART_ONCE_CHILDREN = ["size", "count"]

LINK_SUBPART_PARENTS = ["subpart"]
LINK_SUBPART_CHILDREN = CHILDREN


DECODER = {
    "any": {},
    "clause": {"TEXT": {"NOT_IN": list(".;:,")}},
}


def link_part_patterns():
    return Compiler(
        label="link_part",
        decoder=DECODER
        | {
            "part": {"ENT_TYPE": {"IN": LINK_PART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_PART_CHILDREN}},
        },
        patterns=[
            "trait+ any* part+",
            "part+  any* trait+",
        ],
    )


def link_part_once_patterns():
    return Compiler(
        label="link_part_once",
        decoder=DECODER
        | {
            "part": {"ENT_TYPE": {"IN": LINK_PART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_PART_ONCE_CHILDREN}},
        },
        patterns=[
            "trait+ any* part+",
            "part+  any* trait+",
        ],
    )


def link_subpart_patterns():
    return Compiler(
        label="link_subpart",
        decoder=DECODER
        | {
            "subpart": {"ENT_TYPE": {"IN": LINK_SUBPART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_SUBPART_CHILDREN}},
        },
        patterns=[
            "trait+   clause* subpart+",
            "subpart+ clause* trait+",
        ],
    )


def link_subpart_once_patterns():
    return Compiler(
        label="link_subpart_once",
        decoder=DECODER
        | {
            "part": {"ENT_TYPE": {"IN": LINK_SUBPART_PARENTS}},
            "trait": {"ENT_TYPE": {"IN": LINK_PART_ONCE_CHILDREN}},
        },
        patterns=[
            "trait+ any* part+",
            "part+  any* trait+",
        ],
    )
