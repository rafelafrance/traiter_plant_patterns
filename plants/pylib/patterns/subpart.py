from spacy import registry
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

_DECODER = common.PATTERNS | {
    "part": {"ENT_TYPE": "part"},
    "subpart": {"ENT_TYPE": "subpart"},
}

# ####################################################################################
SUBPART = Compiler(
    "subpart",
    decoder=_DECODER,
    patterns=[
        "subpart - subpart",
        "part - subpart",
        "subpart - part",
    ],
)

# ####################################################################################
SUBPART_SUFFIX = Compiler(
    "subpart_suffix",
    on_match="plant_subpart_suffix_v1",
    decoder=_DECODER,
    patterns=[
        "- subpart",
    ],
)


@registry.misc(SUBPART_SUFFIX.on_match)
def on_subpart_suffix_match(ent):
    ent._.data["subpart_suffix"] = ent.text.lower().replace("-", "").strip()
