from traiter.pylib.matcher_compiler import Compiler
from traiter.pylib.patterns import common

from ..vocabulary import terms

_LOCATION_PARENTS = terms.LOCATION_ENTS
_LOCATION_CHILDREN = terms.all_traits_except(
    " shape sex taxon ".split() + terms.LOCATION_ENTS + terms.NO_LINK_ENTS
)

LOCATION_LINKER = Compiler(
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
    output=None,
)
