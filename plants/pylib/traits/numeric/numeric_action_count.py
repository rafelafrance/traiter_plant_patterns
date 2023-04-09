from spacy import registry
from traiter.pylib import util as t_util
from traiter.pylib.traits import trait_util

from .numeric_action_range import ALL_CSVS
from .numeric_action_range import REPLACE

COUNT_MATCH = "count_match"
COUNT_WORD_MATCH = "count_word_match"

SUFFIX_TERM = trait_util.term_data(ALL_CSVS, "suffix_term")


@registry.misc(COUNT_MATCH)
def count_match(ent):
    per_part = []
    suffix = []
    for token in ent:
        if trait_util.has_data(token) and token._.flag == "range":
            for key, value in token._.data.items():
                ent._.data[key] = t_util.to_positive_int(value)
        if token._.term == "number_word":
            value = REPLACE.get(token.lower_, token.lower_)
            ent._.data["low"] = t_util.to_positive_int(value)
        elif token._.term == "count_suffix":
            suffix.append(token.lower_)
        elif token._.data and token._.flag == "part":
            part_trait = token._.data["trait"]
            ent._.data["per_part"] = token._.data[part_trait]
        elif token._.term == "per_count":
            per_part.append(token.lower_)
        elif token._.term == "missing":
            ent._.data["missing"] = True

    if per_part:
        per_part = " ".join(per_part)
        ent._.data["count_group"] = REPLACE.get(per_part, per_part)

    if suffix:
        suffix = "".join(suffix)
        value = REPLACE.get(suffix, suffix)
        key = SUFFIX_TERM.get(suffix)
        if key:
            ent._.data[key] = value


@registry.misc(COUNT_WORD_MATCH)
def count_word_match(ent):
    ent._.data["low"] = int(REPLACE[ent[0].lower_])
