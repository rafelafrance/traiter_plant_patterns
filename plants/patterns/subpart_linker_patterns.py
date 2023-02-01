"""Link subparts to traits.

We are linking a subpart like "hairs" to a trait like "length" or "color".
For example: "leaves are covered with white hairs 1-(1.5) mm long."
Should link "hairs" with the color "white" and to the length "1 to 1.5 mm".
Named entity recognition (NER) must be run first.
"""
from traiter.patterns import matcher_patterns

from . import common_patterns
from . import term_patterns

# ####################################################################################
SUBPART_PARENTS = ["subpart"]
SUBPART_CHILDREN = term_patterns.all_traits_except(
    " subpart sex reproduction plant_habit habit ".split()
    + term_patterns.LOCATIONS
    + term_patterns.PARTS
    + term_patterns.PLANT_TRAITS
    + term_patterns.NO_LINK
)

SUBPART_LINKER = matcher_patterns.MatcherPatterns(
    "subpart_linker",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "subpart": {"ENT_TYPE": {"IN": SUBPART_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": SUBPART_CHILDREN}},
    },
    patterns=[
        "trait   clause* subpart",
        "subpart clause* trait",
    ],
)

# ####################################################################################
SUBPART_SUFFIX_PARENTS = ["subpart_suffix"]
SUBPART_SUFFIX_CHILDREN = SUBPART_CHILDREN
SUBPART_SUFFIX_LINKER = matcher_patterns.MatcherPatterns(
    "subpart_suffix_linker",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "subpart_suffix": {"ENT_TYPE": {"IN": SUBPART_SUFFIX_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": SUBPART_SUFFIX_CHILDREN}},
    },
    patterns=[
        "trait   subpart_suffix",
        "trait - subpart_suffix",
    ],
)
