from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

from .. import const

_LOCATION_PARENTS = const.LOCATION_ENTS
_LOCATION_CHILDREN = const.all_traits_except(
    " shape sex taxon ".split() + const.LOCATION_ENTS + const.NO_LINK_ENTS
)

LOCATION_LINKER = MatcherPatterns(
    "location_linker",
    on_match=None,
    decoder=common.PATTERNS
    | {
        "location": {"ENT_TYPE": {"IN": _LOCATION_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _LOCATION_CHILDREN}},
    },
    patterns=[
        "trait    clause* location",
        "location clause* trait",
    ],
    terms=const.PLANT_TERMS,
    output=None,
)
