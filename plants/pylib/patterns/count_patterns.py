from spacy import registry
from traiter import actions
from traiter import const as t_const
from traiter import util as t_util
from traiter.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

# ####################################################################################
NOT_COUNT_WORDS = (
    t_const.CROSS
    + t_const.SLASH
    + """ average side times days weeks by table """.split()
)
NOT_COUNT_ENTS = """ imperial_length metric_mass imperial_mass """.split()

EVERY = """ every per each or more """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "adp": {"POS": {"IN": ["ADP"]}},
    "as": {"LOWER": {"IN": ["as"]}},
    "count_word": {"ENT_TYPE": "count_word"},
    "dim": {"ENT_TYPE": "dim"},
    "not_count_ent": {"ENT_TYPE": {"IN": NOT_COUNT_ENTS}},
    "not_count_word": {"LOWER": {"IN": NOT_COUNT_WORDS}},
    "per_count": {"ENT_TYPE": "per_count"},
    "every": {"LOWER": {"IN": EVERY}},
    "part": {"ENT_TYPE": {"IN": term_patterns.PARTS}},
    "x": {"LOWER": {"IN": ["x", "X"]}},
    "=": {"TEXT": {"IN": ["=", ":"]}},
    "°": {"TEXT": {"IN": ["°"]}},
}

# ####################################################################################
COUNT = MatcherPatterns(
    "count",
    on_match="plant_count_v1",
    decoder=DECODER,
    patterns=[
        "99-99",
        "99-99 -* per_count",
        "( 99-99 ) per_count",
        "99-99 -* every+ part per_count?",
        "( 99-99 ) every part",
        "per_count+ adp? 99-99",
    ],
)


@registry.misc(COUNT.on_match)
def on_count_match(ent):
    ent._.new_label = "count"

    range_ = next(t for t in ent if t.ent_type_ == "range")
    ent._.data = range_._.data

    for key in ["min", "low", "high", "max"]:
        if key in ent._.data:
            if ent._.data[key].find(".") > -1:
                raise actions.RejectMatch()
            ent._.data[key] = t_util.to_positive_int(ent._.data[key])

    if ent._.data.get("range"):
        del ent._.data["range"]

    if per_count := next((e for e in ent.ents if e.label_ == "per_count"), None):
        text = per_count.text.lower()
        ent._.data["count_group"] = term_patterns.REPLACE.get(text, text)

    if per_part := next((e for e in ent.ents if e.label_ in term_patterns.PARTS), None):
        text = per_part.text.lower()
        ent._.data["per_part"] = term_patterns.REPLACE.get(text, text)


# ####################################################################################
COUNT_WORD = MatcherPatterns(
    "count_word",
    on_match="plant_count_word_v1",
    decoder=DECODER,
    patterns=[
        "count_word",
    ],
)


@registry.misc(COUNT_WORD.on_match)
def on_count_word_match(ent):
    ent._.new_label = "count"
    word = next(e for e in ent.ents if e.label_ == "count_word")
    word._.data = {
        "low": t_util.to_positive_int(term_patterns.REPLACE[word.text.lower()])
    }


# ####################################################################################
NOT_A_COUNT = MatcherPatterns(
    "not_a_count",
    on_match=actions.REJECT_MATCH,
    decoder=DECODER,
    patterns=[
        "99-99 not_count_ent",
        "99-99 not_count_word 99-99? not_count_ent?",
        "9 / 9",
        "x =? 99-99",
        "99-99 ; 99-99",
        "99-99 :",
        "99-99 any? any? any? as dim",
        "99-99 °",
    ],
)
