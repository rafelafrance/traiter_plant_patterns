"""Link traits to a plant's sex.

We want to handle sexual dimorphism by linking traits to a plant's sex.
For example: "petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate):
Should note that pistillate petals are 3-10 mm and staminate petals are 5-8 mm.
Named entity recognition (NER) must be run first.
"""
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from .. import trait_lists


_SEX_PARENTS = ["sex"]
_SEX_CHILDREN = trait_lists.all_traits_except(["sex"] + trait_lists.NO_LINK)

SEX_LINKER = Compiler(
    "sex_linker",
    decoder=common.PATTERNS
    | {
        "sex": {"ENT_TYPE": {"IN": _SEX_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _SEX_CHILDREN}},
    },
    patterns=[
        "trait phrase* sex",
        "sex   phrase* trait",
    ],
)
