from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from .. import trait_lists

_LOCATION_PARENTS = trait_lists.LOCATIONS
_LOCATION_CHILDREN = trait_lists.all_traits_except(
    " shape sex taxon ".split() + trait_lists.LOCATIONS + trait_lists.NO_LINK
)

LOCATION_LINKER = Compiler(
    "location_linker",
    decoder=common.PATTERNS
    | {
        "location": {"ENT_TYPE": {"IN": _LOCATION_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _LOCATION_CHILDREN}},
    },
    patterns=[
        "trait    clause* location",
        "location clause* trait",
    ],
)
