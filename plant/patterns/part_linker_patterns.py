"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from traiter.patterns import matcher_patterns

from . import common_patterns
from . import term_patterns


# ####################################################################################
PART_PARENTS = term_patterns.PARTS
PART_CHILDREN = term_patterns.all_traits_except(
    ["leaf_duration", "sex", "taxon", "size", "count", "habit"]
    + term_patterns.PARTS
    + term_patterns.LOCATIONS
    + term_patterns.PLANT_TRAITS
)

PART_LINKER = matcher_patterns.MatcherPatterns(
    "part_linker",
    decoder=common_patterns.COMMON_PATTERNS
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
LINK_PART_ONCE = matcher_patterns.MatcherPatterns(
    "link_part_once",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": LINK_PART_ONCE_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LINK_PART_ONCE_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
)
