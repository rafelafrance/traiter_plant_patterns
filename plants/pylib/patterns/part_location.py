from spacy import registry
from traiter.pylib import actions
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from . import size_
from .. import trait_lists
from .terms import PLANT_TERMS

_DECODER = common.PATTERNS | {
    "adj": {"POS": "ADJ"},
    "cm": {"ENT_TYPE": "metric_length"},
    "joined": {"ENT_TYPE": "joined"},
    "leader": {"LOWER": {"IN": """to at embracing immersed from""".split()}},
    "location": {"ENT_TYPE": {"IN": trait_lists.LOCATIONS}},
    "of": {"LOWER": "of"},
    "part": {"ENT_TYPE": {"IN": trait_lists.PARTS}},
    "prep": {"POS": "ADP"},
    "sex": {"ENT_TYPE": "sex"},
    "subpart": {"ENT_TYPE": "subpart"},
}


def get_joined(ent):
    if joined := [e for e in ent.ents if e.label_ == "joined"]:
        text = joined[0].text.lower()
        return PLANT_TERMS.replace.get(text, text)
    return ""


# ####################################################################################
_ON_AS_LOCATION_MATCH = "plant_as_location_v1"

PART_AS_LOCATION = Compiler(
    "part_as_loc",
    on_match=_ON_AS_LOCATION_MATCH,
    decoder=_DECODER,
    patterns=[
        "joined?  leader part",
        "location leader part",
        "leader prep part",
    ],
)

SUBPART_AS_LOCATION = Compiler(
    "subpart_as_loc",
    on_match=_ON_AS_LOCATION_MATCH,
    decoder=_DECODER,
    patterns=[
        "joined?  leader subpart",
        "joined?  leader subpart of adj? subpart",
        "location leader subpart",
        "location leader subpart of adj? subpart",
    ],
)


@registry.misc(_ON_AS_LOCATION_MATCH)
def on_as_location_match(ent):
    if joined := get_joined(ent):
        ent._.data["joined"] = joined
    actions.text_action(ent)


# ####################################################################################
PART_AS_DISTANCE = Compiler(
    "part_as_distance",
    on_match="plant_part_as_distance_v1",
    decoder=_DECODER,
    patterns=[
        "joined?  leader part prep? 99-99 cm",
        "location leader part prep? 99-99 cm",
    ],
)


@registry.misc(PART_AS_DISTANCE.on_match)
def on_part_as_distance_match(ent):
    if joined := get_joined(ent):
        ent._.data["joined"] = joined
    size_.on_size_match(ent)
    ent._.new_label = "part_as_loc"
