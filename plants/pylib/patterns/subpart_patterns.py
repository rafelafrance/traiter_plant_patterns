from spacy import registry
from traiter.pylib.pattern_compilers.matcher_compiler import MatcherCompiler
from traiter.pylib.patterns import common_patterns

DECODER = common_patterns.COMMON_PATTERNS | {
    "part": {"ENT_TYPE": "part"},
    "subpart": {"ENT_TYPE": "subpart"},
}

# ####################################################################################
SUBPART = MatcherCompiler(
    "subpart",
    decoder=DECODER,
    patterns=[
        "subpart - subpart",
        "part - subpart",
        "subpart - part",
    ],
)

# ####################################################################################
SUBPART_SUFFIX = MatcherCompiler(
    "subpart_suffix",
    on_match="plant_subpart_suffix_v1",
    decoder=DECODER,
    patterns=[
        "- subpart",
    ],
)


@registry.misc(SUBPART_SUFFIX.on_match)
def on_subpart_suffix_match(ent):
    ent._.data["subpart_suffix"] = ent.text.lower().replace("-", "").strip()
