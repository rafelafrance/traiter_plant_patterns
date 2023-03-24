from spacy import registry
from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

from .. import const

_DECODER = common.PATTERNS | {
    "part": {"ENT_TYPE": "part"},
    "subpart": {"ENT_TYPE": "subpart"},
}

# ####################################################################################
SUBPART = MatcherPatterns(
    "subpart",
    on_match=None,
    decoder=_DECODER,
    patterns=[
        "subpart - subpart",
        "part - subpart",
        "subpart - part",
    ],
    terms=const.PLANT_TERMS,
    output=["subpart"],
)

# ####################################################################################
SUBPART_SUFFIX = MatcherPatterns(
    "subpart_suffix",
    on_match="plant_subpart_suffix_v1",
    decoder=_DECODER,
    patterns=[
        "- subpart",
    ],
    terms=const.PLANT_TERMS,
    output=["subpart_suffix"],
)


@registry.misc(SUBPART_SUFFIX.on_match)
def on_subpart_suffix_match(ent):
    ent._.data["subpart_suffix"] = ent.text.lower().replace("-", "").strip()
