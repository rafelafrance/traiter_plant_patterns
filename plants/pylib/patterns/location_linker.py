from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

import plants.pylib.trait_lists
from . import term

LOCATION_PARENTS = plants.pylib.trait_lists.LOCATIONS
LOCATION_CHILDREN = plants.pylib.trait_lists.all_traits_except(
    " shape sex taxon ".split()
    + plants.pylib.trait_lists.LOCATIONS
    + plants.pylib.trait_lists.NO_LINK
)

LOCATION_LINKER = Compiler(
    "location_linker",
    decoder=common.PATTERNS
    | {
        "location": {"ENT_TYPE": {"IN": LOCATION_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": LOCATION_CHILDREN}},
    },
    patterns=[
        "trait    clause* location",
        "location clause* trait",
    ],
)
