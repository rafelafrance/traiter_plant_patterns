from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from . import terms

_LOCATION_PARENTS = terms.LOCATIONS
_LOCATION_CHILDREN = terms.all_traits_except(
    " shape sex taxon ".split() + terms.LOCATIONS + terms.NO_LINK
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
