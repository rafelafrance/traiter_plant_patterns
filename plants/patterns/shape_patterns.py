import re

from spacy import registry
from traiter import const as t_const
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns


TEMP = ["\\" + c for c in t_const.DASH[:2]]
MULTIPLE_DASHES = rf'[{"".join(TEMP)}]{{2,}}'

SHAPE_LOC = ["shape", "shape_leader", "location"]
SHAPE_WORD = ["shape", "shape_leader"]

DECODER = common_patterns.COMMON_PATTERNS | {
    "shape": {"ENT_TYPE": "shape"},
    "shape_leader": {"ENT_TYPE": "shape_leader"},
    "shape_loc": {"ENT_TYPE": {"IN": SHAPE_LOC}},
    "shape_word": {"ENT_TYPE": {"IN": SHAPE_WORD}},
    "angular": {"LOWER": {"IN": ["angular", "angulate"]}},
}


# #####################################################################################
SHAPE = MatcherPatterns(
    "shape",
    on_match="plant_shape_v1",
    decoder=DECODER,
    patterns=[
        "shape_loc* -* shape+",
        "shape_loc* -* shape -* shape+",
        "shape_leader -/to shape_word+ -* shape+",
        "shape_word+ -* shape+",
    ],
)


@registry.misc(SHAPE.on_match)
def on_shape_match(ent):
    # Sets do not preserve order
    cached_labels = ["shape", "shape_suffix"]
    parts = {
        r: 1
        for t in ent
        if (r := term_patterns.REPLACE.get(t.lower_, t.lower_))
        and t._.cached_label in cached_labels
    }

    value = "-".join(parts.keys())
    value = re.sub(rf"\s*{MULTIPLE_DASHES}\s*", r"-", value)
    ent._.new_label = "shape"
    ent._.data["shape"] = term_patterns.REPLACE.get(value, value)
    loc = [t.lower_ for t in ent if t._.cached_label == "location"]
    if loc:
        ent._.data["location"] = loc[0]


# #####################################################################################
N_SHAPE = MatcherPatterns(
    "n_shape",
    on_match="plant_n_shape_v1",
    decoder=DECODER,
    patterns=[
        "shape_loc* 9 - angular",
    ],
)


@registry.misc(N_SHAPE.on_match)
def on_n_shape_match(ent):
    """Handle 5-angular etc."""
    ent._.new_label = "shape"
    ent._.data = {"shape": "polygonal"}
