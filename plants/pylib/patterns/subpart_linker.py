"""Link subparts to traits.

We are linking a subpart like "hairs" to a trait like "length" or "color".
For example: "leaves are covered with white hairs 1-(1.5) mm long."
Should link "hairs" with the color "white" and to the length "1 to 1.5 mm".
Named entity recognition (NER) must be run first.
"""
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from .. import trait_lists

# ####################################################################################
_SUBPART_PARENTS = ["subpart"]
_SUBPART_CHILDREN = trait_lists.all_traits_except(
    " subpart sex reproduction plant_habit habit ".split()
    + trait_lists.LOCATIONS
    + trait_lists.PARTS
    + trait_lists.PLANT_TRAITS
    + trait_lists.NO_LINK
)

SUBPART_LINKER = Compiler(
    "subpart_linker",
    decoder=common.PATTERNS
    | {
        "subpart": {"ENT_TYPE": {"IN": _SUBPART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _SUBPART_CHILDREN}},
    },
    patterns=[
        "trait   clause* subpart",
        "subpart clause* trait",
    ],
)

# ####################################################################################
_SUBPART_SUFFIX_PARENTS = ["subpart_suffix"]
_SUBPART_SUFFIX_CHILDREN = _SUBPART_CHILDREN

SUBPART_SUFFIX_LINKER = Compiler(
    "subpart_suffix_linker",
    decoder=common.PATTERNS
    | {
        "subpart_suffix": {"ENT_TYPE": {"IN": _SUBPART_SUFFIX_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _SUBPART_SUFFIX_CHILDREN}},
    },
    patterns=[
        "trait   subpart_suffix",
        "trait - subpart_suffix",
    ],
)
