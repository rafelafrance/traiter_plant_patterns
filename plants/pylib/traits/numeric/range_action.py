import re
from pathlib import Path

from spacy import registry
from traiter.pylib.traits import terms
from traiter.pylib.traits import trait_util

from .. import misc
from .. import part

RANGE_MATCH = "range_match"


MOST_CSVS = [
    Path(__file__).parent / "numeric_terms.csv",
    Path(misc.__file__).parent / "missing_terms.csv",
    Path(misc.__file__).parent / "sex_terms.csv",
    Path(terms.__file__).parent / "unit_distance_terms.csv",
    Path(terms.__file__).parent / "unit_length_terms.csv",
    Path(terms.__file__).parent / "unit_mass_terms.csv",
    Path(terms.__file__).parent / "numeric_terms.csv",
    Path(terms.__file__).parent / "month_terms.csv",
]
PART_CSV = Path(part.__file__).parent / "part_terms.csv"
ALL_CSVS = MOST_CSVS + [PART_CSV]

REPLACE = trait_util.term_data(ALL_CSVS, "replace")


@registry.misc(RANGE_MATCH)
def range_match(ent):
    nums = []
    for token in ent:
        token._.flag = "range"
        nums += re.findall(r"\d*\.?\d+", token.text)

    # Cache the values in the first token
    keys = ent.label_.split(".")[1:]
    ent[0]._.data = {k: v for k, v in zip(keys, nums)}
    ent[0]._.flag = "range_data"
