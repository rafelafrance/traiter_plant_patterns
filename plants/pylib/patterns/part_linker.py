"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from . import terms


# ####################################################################################
_PART_PARENTS = terms.PARTS
_PART_CHILDREN = terms.all_traits_except(
    ["leaf_duration", "sex", "taxon", "size", "count", "habit"]
    + terms.PARTS
    + terms.LOCATIONS
    + terms.PLANT_TRAITS
    + terms.NO_LINK
)

PART_LINKER = Compiler(
    "part_linker",
    decoder=common.PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": _PART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _PART_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)

# ####################################################################################
_LINK_PART_ONCE_PARENTS = _PART_PARENTS
_LINK_PART_ONCE_CHILDREN = ["size", "count"]

LINK_PART_ONCE = Compiler(
    "link_part_once",
    decoder=common.PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": _LINK_PART_ONCE_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _LINK_PART_ONCE_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)
