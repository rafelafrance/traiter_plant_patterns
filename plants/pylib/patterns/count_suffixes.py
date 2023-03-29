from spacy import registry
from traiter.pylib import actions
from traiter.pylib import util as t_util
from traiter.pylib.matcher_compiler import Compiler
from traiter.pylib.patterns import common

from ..vocabulary import terms


_COUNT_WORDS = ["count_word", "number_word"]
_SUFFIX_TERMS = terms.PLANT_TERMS.pattern_dict("suffix_term")


_DECODER = common.PATTERNS | {
    "count_suffix": {"ENT_TYPE": "count_suffix"},
    "count_word": {"ENT_TYPE": {"IN": _COUNT_WORDS}},
}

# ####################################################################################
COUNT_SUFFIX = Compiler(
    "count_suffix",
    on_match="plant_count_suffix_v1",
    decoder=_DECODER,
    patterns=[
        "99-99 count_suffix",
    ],
    output=["count"],
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

    label = _SUFFIX_TERMS.get(suffix.lower_, "subpart")
    suffix = terms.PLANT_TERMS.replace.get(suffix.lower_, suffix.lower_)
    ent._.data[label] = suffix


# ####################################################################################
COUNT_SUFFIX_WORD = Compiler(
    "count_suffix_word",
    on_match="plant_count_suffix_word_v1",
    decoder=_DECODER,
    patterns=[
        "count_word count_suffix",
    ],
    output=["count"],
)


@registry.misc(COUNT_SUFFIX_WORD.on_match)
def on_count_suffix_word_match(ent):
    ent._.new_label = "count"

    word = next(e for e in ent.ents if e.label_ in _COUNT_WORDS)
    ent._.data["low"] = t_util.to_positive_int(
        terms.PLANT_TERMS.replace[word.text.lower()]
    )

    if not (suffix := next((t for t in ent if t.ent_type_ == "count_suffix"), None)):
        raise actions.RejectMatch()
    lower = suffix.text.lower()
    label = _SUFFIX_TERMS.get(lower, "subpart")
    ent._.data[label] = terms.PLANT_TERMS.replace.get(lower, lower)
