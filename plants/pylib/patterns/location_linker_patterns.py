from traiter.patterns import matcher_patterns

from . import common_patterns
from . import term_patterns

LOCATION_PARENTS = term_patterns.LOCATIONS
LOCATION_CHILDREN = term_patterns.all_traits_except(
    " shape sex taxon ".split() + term_patterns.LOCATIONS + term_patterns.NO_LINK
)

LOCATION_LINKER = matcher_patterns.MatcherPatterns(
    "location_linker",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "location": {"ENT_TYPE": {"IN": LOCATION_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LOCATION_CHILDREN}},
    },
    patterns=[
        "trait    clause* location",
        "location clause* trait",
    ],
)
