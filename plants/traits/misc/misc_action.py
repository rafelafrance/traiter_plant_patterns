from pathlib import Path

from spacy import registry
from traiter.traits import trait_util

MISC_MATCH = "misc_match"

ALL_CSVS = list(Path(__file__).parent.glob("*.csv"))

REPLACE = trait_util.term_data(ALL_CSVS, "replace")
LABELS = trait_util.get_labels(ALL_CSVS)


@registry.misc(MISC_MATCH)
def misc_match(ent):
    frags = []
    relabel = ""
    for token in ent:
        relabel = token._.term
        if token.text not in "[]()":
            frags.append(REPLACE.get(token.lower_, token.lower_))
    ent._.relabel = relabel
    ent._.data[relabel] = " ".join(frags)
