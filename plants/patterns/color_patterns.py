import re

from spacy import registry
from traiter import actions
from traiter import const as t_const
from traiter.patterns import matcher_patterns

from . import common_patterns
from . import term_patterns
from .. import const

MULTIPLE_DASHES = ["\\" + c for c in t_const.DASH_CHAR]
MULTIPLE_DASHES = rf'\s*[{"".join(MULTIPLE_DASHES)}]{{2,}}\s*'

SKIP = t_const.DASH + common_patterns.MISSING

COLOR = matcher_patterns.MatcherPatterns(
    "color",
    on_match="plant_color_v1",
    decoder=common_patterns.COMMON_PATTERNS
    | {
        "color_words": {"ENT_TYPE": {"IN": ["color", "color_mod"]}},
        "color": {"ENT_TYPE": "color"},
        "to": {"POS": {"IN": ["AUX"]}},
    },
    patterns=[
        "missing? color_words* -* color+ -* color_words*",
        "missing? color_words+ to color_words+ color+ -* color_words*",
    ],
)


@registry.misc(COLOR.on_match)
def on_color_match(ent):
    parts = []
    for token in ent:
        replace = term_patterns.REPLACE.get(token.lower_, token.lower_)
        if replace in SKIP:
            continue
        if term_patterns.REMOVE.get(token.lower_):
            continue
        if token.pos_ in ["AUX"]:
            continue
        if token.shape_ in const.TITLE_SHAPES:
            continue
        parts.append(replace)

    if not parts:
        ent._.delete = True
        raise actions.RejectMatch()

    value = "-".join(parts)
    value = re.sub(MULTIPLE_DASHES, r"-", value)
    ent._.data["color"] = term_patterns.REPLACE.get(value, value)
    if any(t for t in ent if t.lower_ in common_patterns.MISSING):
        ent._.data["missing"] = True
