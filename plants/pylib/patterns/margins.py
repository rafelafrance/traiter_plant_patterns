import re

from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib.matcher_compiler import Compiler
from traiter.pylib.patterns import common

from ..vocabulary import terms

_TEMP = ["\\" + c for c in t_const.DASH[:2]]

_LEADERS = """ shape shape_leader margin_leader """.split()
_FOLLOWERS = """ margin margin_follower """.split()
_SHAPES = """ margin shape """.split()

MARGIN = Compiler(
    "margin",
    on_match="plant_margin_v1",
    decoder=common.PATTERNS
    | {
        "margin": {"ENT_TYPE": "margin"},
        "shape": {"ENT_TYPE": "shape"},
        "leader": {"ENT_TYPE": {"IN": _LEADERS}},
        "follower": {"ENT_TYPE": {"IN": _FOLLOWERS}},
    },
    patterns=[
        "leader* -* margin+",
        "leader* -* margin -* follower*",
        "leader* -* margin -* shape? follower+ shape?",
        "shape+ -* follower+",
    ],
    output=["margin"],
)


@registry.misc(MARGIN.on_match)
def on_margin_match(ent):
    multi_dashes = rf'[{"".join(_TEMP)}]{{2,}}'
    value = {
        r: 1
        for t in ent
        if (r := terms.PLANT_TERMS.replace.get(t.text, t.text))
        and t._.cached_label in ["margin", "shape"]
    }
    value = "-".join(value.keys())
    value = re.sub(rf"\s*{multi_dashes}\s*", r"-", value)
    ent._.data["margin"] = terms.PLANT_TERMS.replace.get(value, value)
