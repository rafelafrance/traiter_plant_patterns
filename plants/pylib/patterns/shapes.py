import re

from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

from .. import const

_SHAPE_LOC = ["shape", "shape_leader", "location"]
_SHAPE_WORD = ["shape", "shape_leader"]

_TEMP = ["\\" + c for c in t_const.DASH[:2]]
_MULTIPLE_DASHES = rf'[{"".join(_TEMP)}]{{2,}}'

_DECODER = common.PATTERNS | {
    "shape": {"ENT_TYPE": "shape"},
    "shape_leader": {"ENT_TYPE": "shape_leader"},
    "shape_loc": {"ENT_TYPE": {"IN": _SHAPE_LOC}},
    "shape_word": {"ENT_TYPE": {"IN": _SHAPE_WORD}},
    "angular": {"LOWER": {"IN": ["angular", "angulate"]}},
}


# #####################################################################################
SHAPE = MatcherPatterns(
    "shape",
    on_match="plant_shape_v1",
    decoder=_DECODER,
    patterns=[
        "shape_loc* -* shape+",
        "shape_loc* -* shape -* shape+",
        "shape_leader -/to shape_word+ -* shape+",
        "shape_word+ -* shape+",
    ],
    terms=const.PLANT_TERMS,
    output=["shape"],
)


@registry.misc(SHAPE.on_match)
def on_shape_match(ent):
    cached_labels = ["shape", "shape_suffix"]

    # Sets do not preserve order
    parts = {
        r: 1
        for t in ent
        if (r := const.PLANT_TERMS.replace.get(t.lower_, t.lower_))
        and t._.cached_label in cached_labels
    }

    value = "-".join(parts.keys())
    value = re.sub(rf"\s*{_MULTIPLE_DASHES}\s*", r"-", value)
    ent._.new_label = "shape"
    ent._.data["shape"] = const.PLANT_TERMS.replace.get(value, value)
    loc = [t.lower_ for t in ent if t._.cached_label == "location"]
    if loc:
        ent._.data["location"] = loc[0]


# #####################################################################################
N_SHAPE = MatcherPatterns(
    "n_shape",
    on_match="plant_n_shape_v1",
    decoder=_DECODER,
    patterns=[
        "shape_loc* 9 - angular",
    ],
    terms=const.PLANT_TERMS,
    output=["shape"],
)


@registry.misc(N_SHAPE.on_match)
def on_n_shape_match(ent):
    """Handle 5-angular etc."""
    ent._.new_label = "shape"
    ent._.data = {"shape": "polygonal"}
