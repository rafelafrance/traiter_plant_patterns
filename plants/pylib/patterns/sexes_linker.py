"""Link traits to a plant's sex.

We want to handle sexual dimorphism by linking traits to a plant's sex.
For example: "petals (1–)3–10(–12) mm (pistillate) or 5–8(–10) mm (staminate):
Should note that pistillate petals are 3-10 mm and staminate petals are 5-8 mm.
Named entity recognition (NER) must be run first.
"""
from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

from .. import const


_SEX_PARENTS = ["sex"]
_SEX_CHILDREN = const.all_traits_except(["sex"] + const.NO_LINK_ENTS)

SEX_LINKER = MatcherPatterns(
    "sex_linker",
    on_match=None,
    decoder=common.PATTERNS
    | {
        "sex": {"ENT_TYPE": {"IN": _SEX_PARENTS}},
        "trait": {"ENT_TYPE": {"IN": _SEX_CHILDREN}},
    },
    patterns=[
        "trait phrase* sex",
        "sex   phrase* trait",
    ],
    terms=const.PLANT_TERMS,
    output=None,
)
