from spacy.util import registry
from traiter.pylib.actions import REJECT_MATCH
from traiter.pylib.pattern_compilers.matcher import Compiler

from . import common

_NOPE = """ of gps ° elev """.split()

_DECODER = common.PATTERNS | {
    "jr": {"ENT_TYPE": "name_suffix"},
    "dr": {"ENT_TYPE": "name_prefix"},
    "person": {"ENT_TYPE": "PERSON"},
    "maybe": {"POS": "PROPN"},
    "conflict": {"ENT_TYPE": "us_county"},
    "nope": {"LOWER": {"IN": _NOPE}},
    "A": {"TEXT": {"REGEX": r"^[A-Z][._,]?$"}},
    "_": {"TEXT": {"REGEX": r"^[._,]+$"}},
}

NAME = Compiler(
    "name",
    on_match="digi_leap.name.v1",
    decoder=_DECODER,
    patterns=[
        "dr? person+              _? jr",
        "dr? person+  _? person   _? jr",
        "dr? person+  _? conflict _? jr",
        "dr? conflict _? person   _? jr",
        "dr? person+                   ",
        "dr? person+  _? person        ",
        "dr? A A? maybe",
        "dr? A A? maybe _? jr",
    ],
)


@registry.misc(NAME.on_match)
def on_name_match(ent):
    if ent._.data.get("PERSON"):
        del ent._.data["PERSON"]


# ####################################################################################
NOT_name = Compiler(
    "not_name",
    on_match=REJECT_MATCH,
    decoder=_DECODER,
    patterns=[
        "         nope+ ",
        "         nope  person+ ",
        "         nope  maybe+ ",
        " person+ nope+ ",
        " maybe+  nope+ ",
        " person+ nope  person+",
        " maybe+  nope  person+",
        " person+ nope  maybe+",
        " maybe+  nope  maybe+",
    ],
)
