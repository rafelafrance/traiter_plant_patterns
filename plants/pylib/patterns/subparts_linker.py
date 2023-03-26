"""Link subparts to traits.

We are linking a subpart like "hairs" to a trait like "length" or "color".
For example: "leaves are covered with white hairs 1-(1.5) mm long."
Should link "hairs" with the color "white" and to the length "1 to 1.5 mm".
Named entity recognition (NER) must be run first.
"""
from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

from ..vocabulary import terms

# ####################################################################################
_SUBPART_PARENTS = ["subpart"]
_SUBPART_CHILDREN = terms.all_traits_except(
    " subpart sex reproduction plant_habit habit ".split()
    + terms.LOCATION_ENTS
    + terms.PART_ENTS
    + terms.PLANT_ENTS
    + terms.NO_LINK_ENTS
)

SUBPART_LINKER = MatcherPatterns(
    "subpart_linker",
    on_match=None,
    decoder=common.PATTERNS
    | {
        "subpart": {"ENT_TYPE": {"IN": _SUBPART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _SUBPART_CHILDREN}},
    },
    patterns=[
        "trait   clause* subpart",
        "subpart clause* trait",
    ],
    output=None,
)

# ####################################################################################
_SUBPART_SUFFIX_PARENTS = ["subpart_suffix"]
_SUBPART_SUFFIX_CHILDREN = _SUBPART_CHILDREN

SUBPART_SUFFIX_LINKER = MatcherPatterns(
    "subpart_suffix_linker",
    on_match=None,
    decoder=common.PATTERNS
    | {
        "subpart_suffix": {"ENT_TYPE": {"IN": _SUBPART_SUFFIX_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _SUBPART_SUFFIX_CHILDREN}},
    },
    patterns=[
        "trait   subpart_suffix",
        "trait - subpart_suffix",
    ],
    output=None,
)
