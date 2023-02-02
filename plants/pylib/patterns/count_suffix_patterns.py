from spacy import registry
from traiter.pylib import actions
from traiter.pylib import util as t_util
from traiter.pylib.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns

COUNT_WORDS = ["count_word", "number_word"]

DECODER = common_patterns.COMMON_PATTERNS | {
    "count_suffix": {"ENT_TYPE": "count_suffix"},
    "count_word": {"ENT_TYPE": {"IN": COUNT_WORDS}},
}


# ####################################################################################
COUNT_SUFFIX = MatcherPatterns(
    "count_suffix",
    on_match="plant_count_suffix_v1",
    decoder=DECODER,
    patterns=[
        "99-99 count_suffix",
    ],
)


@registry.misc(COUNT_SUFFIX.on_match)
def on_count_suffix_match(ent):
    ent._.new_label = "count"
    range_ = next(t for t in ent if t.ent_type_ == "range")
    suffix = next(t for t in ent if t.ent_type_ == "count_suffix")

    ent._.data = range_._.data

    for key in ["min", "low", "high", "max"]:
        if key in ent._.data:
            ent._.data[key] = t_util.to_positive_int(ent._.data[key])

    if ent._.data.get("range"):
        del ent._.data["range"]

    lower = suffix.text.lower()
    label = term_patterns.SUFFIX_TERM.get(lower, "subpart")
    ent._.data[label] = term_patterns.REPLACE.get(lower, lower)


# ####################################################################################
COUNT_SUFFIX_WORD = MatcherPatterns(
    "count_suffix_word",
    on_match="plant_count_suffix_word_v1",
    decoder=DECODER,
    patterns=[
        "count_word count_suffix",
    ],
)


@registry.misc(COUNT_SUFFIX_WORD.on_match)
def on_count_suffix_word_match(ent):
    ent._.new_label = "count"

    word = next(e for e in ent.ents if e.label_ in COUNT_WORDS)
    ent._.data["low"] = t_util.to_positive_int(term_patterns.REPLACE[word.text.lower()])

    if not (suffix := next((t for t in ent if t.ent_type_ == "count_suffix"), None)):
        raise actions.RejectMatch()
    lower = suffix.text.lower()
    label = term_patterns.SUFFIX_TERM.get(lower, "subpart")
    ent._.data[label] = term_patterns.REPLACE.get(lower, lower)
