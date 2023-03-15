"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

import plants.pylib.trait_lists
from . import term


# ####################################################################################
PART_PARENTS = plants.pylib.trait_lists.PARTS
PART_CHILDREN = plants.pylib.trait_lists.all_traits_except(
    ["leaf_duration", "sex", "taxon", "size", "count", "habit"]
    + plants.pylib.trait_lists.PARTS
    + plants.pylib.trait_lists.LOCATIONS
    + plants.pylib.trait_lists.PLANT_TRAITS
    + plants.pylib.trait_lists.NO_LINK
)

PART_LINKER = Compiler(
    "part_linker",
    decoder=common.PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": PART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": PART_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)

# ####################################################################################
LINK_PART_ONCE_PARENTS = PART_PARENTS
LINK_PART_ONCE_CHILDREN = ["size", "count"]
LINK_PART_ONCE = Compiler(
    "link_part_once",
    decoder=common.PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": LINK_PART_ONCE_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LINK_PART_ONCE_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)
