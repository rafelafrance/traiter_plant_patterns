from pathlib import Path

from spacy import registry
from traiter.pylib.traits import trait_util

HABIT_MATCH = "habit_match"

HABIT_CSV = Path(__file__).parent / "habit_terms.csv"

REPLACE = trait_util.term_data(HABIT_CSV, "replace")


@registry.misc(HABIT_MATCH)
def habit_match(ent):
    frags = [REPLACE.get(t.lower_, t.lower_) for t in ent]
    ent._.data = {"habit": " ".join(frags)}
