from spacy import registry
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns

DECODER = common_patterns.COMMON_PATTERNS | {
    "part": {"ENT_TYPE": "part"},
    "subpart": {"ENT_TYPE": "subpart"},
}

# ####################################################################################
SUBPART = MatcherPatterns(
    "subpart",
    decoder=DECODER,
    patterns=[
        "subpart - subpart",
        "part - subpart",
        "subpart - part",
    ],
)

# ####################################################################################
SUBPART_SUFFIX = MatcherPatterns(
    "subpart_suffix",
    on_match="plant.subpart_suffix.v1",
    decoder=DECODER,
    patterns=[
        "- subpart",
    ],
)


@registry.misc(SUBPART_SUFFIX.on_match)
def on_subpart_suffix_match(ent):
    ent._.data["subpart_suffix"] = ent.text.lower().replace("-", "").strip()
