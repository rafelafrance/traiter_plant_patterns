from spacy import registry
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from ..trait_lists import PARTS
from ..trait_lists import PARTS_SET
from ..trait_lists import SUBPARTS
from .terms import PLANT_TERMS

_PART_LEADER = """ primary secondary """.split()

_DECODER = common.PATTERNS | {
    "leader": {"LOWER": {"IN": _PART_LEADER}},
    "part": {"ENT_TYPE": {"IN": PARTS}},
    "subpart": {"ENT_TYPE": {"IN": SUBPARTS}},
}

# ####################################################################################
PART = Compiler(
    "part",
    on_match="plant_part_v1",
    decoder=_DECODER,
    patterns=[
        "leader? part",
        "leader? part -? part",
        "leader? part -? subpart",
        "leader? part    subpart+",
    ],
)


@registry.misc(PART.on_match)
def on_part_match(ent):
    words = []
    new_label = None

    for token in ent:
        label = token._.cached_label
        if label in PARTS:
            new_label = label

        words.append(PLANT_TERMS.replace.get(token.lower_, token.lower_))

    ent._.data[new_label] = " ".join(words)
    ent._.data[new_label] = ent._.data[new_label].replace(" - ", "-")
    ent._.new_label = new_label


# ####################################################################################
MULTIPLE_PARTS = Compiler(
    "multiple_parts",
    on_match="plant_multiple_parts_v1",
    decoder=_DECODER,
    patterns=[
        "leader? part and part",
    ],
)


@registry.misc(MULTIPLE_PARTS.on_match)
def on_multiple_parts_match(ent):
    ent._.new_label = "multiple_parts"
    ent._.data["multiple_parts"] = [
        PLANT_TERMS.replace.get(t.lower_, t.lower_)
        for t in ent
        if t._.cached_label in PARTS_SET
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
        ent._.data["part"] = PLANT_TERMS.replace.get(part.lower_, part.lower_)
    ent._.data["missing_part"] = ent.text.lower()
