from spacy import registry
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

import plants.pylib.trait_lists
from . import term

PART_LEADER = """ primary secondary """.split()

_DECODER = common.PATTERNS | {
    "leader": {"LOWER": {"IN": PART_LEADER}},
    "part": {"ENT_TYPE": {"IN": plants.pylib.trait_lists.PARTS}},
    "subpart": {"ENT_TYPE": {"IN": plants.pylib.trait_lists.SUBPARTS}},
}

# ####################################################################################
PART = Compiler(
    "part",
    on_match="plant_part_v1",
    decoder=_DECODER,
    patterns=[
        "leader  part",
        "leader? part -?  part",
        "leader? part -?  subpart",
        "leader? part     subpart+",
        "leader? part and part",
    ],
)


@registry.misc(PART.on_match)
def on_part_match(ent):
    if any(t._.cached_label in plants.pylib.trait_lists.SUBPARTS for t in ent):
        ent._.new_label = next(t._.cached_label for t in ent)
    elif any(t.lower_ in common.AND for t in ent):
        ent._.new_label = "multiple_parts"
        ent._.data["multiple_parts"] = [
            term_patterns.REPLACE.get(t.lower_, t.lower_)
            for t in ent
            if t.ent_type_ in plants.pylib.trait_lists.PARTS_SET
        ]


# ####################################################################################
MISSING_PART = Compiler(
    "missing_part",
    on_match="plant_missing_part_v1",
    decoder=_DECODER,
    patterns=[
        "missing part",
        "missing part  -  part",
        "missing part and part",
        "missing part -?  subpart",
        "missing part     subpart",
    ],
)


@registry.misc(MISSING_PART.on_match)
def missing_part_match(ent):
    if part := next((t for t in ent if t.ent_type_ == "part"), None):
        ent._.data["part"] = part.lower_
