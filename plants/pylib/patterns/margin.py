import re

from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from . import term

TEMP = ["\\" + c for c in t_const.DASH[:2]]

LEADERS = """ shape shape_leader margin_leader """.split()
FOLLOWERS = """ margin margin_follower """.split()
SHAPES = """ margin shape """.split()

MARGIN = Compiler(
    "margin",
    on_match="plant_margin_v1",
    decoder=common.PATTERNS
    | {
        "margin": {"ENT_TYPE": "margin"},
        "shape": {"ENT_TYPE": "shape"},
        "leader": {"ENT_TYPE": {"IN": LEADERS}},
        "follower": {"ENT_TYPE": {"IN": FOLLOWERS}},
    },
    patterns=[
        "leader* -* margin+",
        "leader* -* margin -* follower*",
        "leader* -* margin -* shape? follower+ shape?",
        "shape+ -* follower+",
    ],
)


@registry.misc(MARGIN.on_match)
def on_margin_match(ent):
    multi_dashes = rf'[{"".join(TEMP)}]{{2,}}'
    value = {
        r: 1
        for t in ent
        if (r := term_patterns.REPLACE.get(t.text, t.text))
        and t._.cached_label in ["margin", "shape"]
    }
    value = "-".join(value.keys())
    value = re.sub(rf"\s*{multi_dashes}\s*", r"-", value)
    ent._.data["margin"] = term_patterns.REPLACE.get(value, value)
