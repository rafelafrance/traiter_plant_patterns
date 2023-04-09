from pathlib import Path

from spacy import registry
from traiter.pylib.traits import trait_util

PART_LOCATION_MATCH = "part_location_match"

PART_LOCATION_CSV = Path(__file__).parent / "part_location_terms.csv"
REPLACE = trait_util.term_data(PART_LOCATION_CSV, "replace")


@registry.misc(PART_LOCATION_MATCH)
def part_location_match(ent):
    frags = []
    for token in ent:
        frag = REPLACE.get(token.lower_, token.lower_)
        frags.append(frag)
    ent._.data[ent.label_] = " ".join(frags)
