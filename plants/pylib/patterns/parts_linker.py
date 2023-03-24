"""Link traits to plant parts.

We are linking parts like "petal" or "leaf" to traits like color or size.
For example: "with thick, woody rootstock" should link the "rootstock" part with
the "woody" trait.
"""
from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

from .. import const

# ####################################################################################
_PART_PARENTS = const.PART_ENTS
_PART_CHILDREN = const.all_traits_except(
    ["leaf_duration", "sex", "taxon", "size", "count", "habit"]
    + const.PART_ENTS
    + const.LOCATION_ENTS
    + const.PLANT_ENTS
    + const.NO_LINK_ENTS
)

PART_LINKER = MatcherPatterns(
    "part_linker",
    on_match=None,
    decoder=common.PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": _PART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _PART_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
    terms=const.PLANT_TERMS,
    output=None,
)

# ####################################################################################
_LINK_PART_ONCE_PARENTS = _PART_PARENTS
_LINK_PART_ONCE_CHILDREN = ["size", "count"]

LINK_PART_ONCE = MatcherPatterns(
    "link_part_once",
    on_match=None,
    decoder=common.PATTERNS
    | {
        "part": {"ENT_TYPE": {"IN": _LINK_PART_ONCE_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _LINK_PART_ONCE_CHILDREN}},
    },
    patterns=[
        "trait any* part",
        "part  any* trait",
    ],
    terms=const.PLANT_TERMS,
    output=None,
)
