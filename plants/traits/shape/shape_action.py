import re
from pathlib import Path

from spacy import registry
from traiter.traits import trait_util

SHAPE_MATCH = "shape_match"
SHAPE_CSV = Path(__file__).parent / "shape_terms.csv"

REPLACE = trait_util.term_data(SHAPE_CSV, "replace")


@registry.misc(SHAPE_MATCH)
def shape_match(ent):

    # Handle 3-angular etc.
    if re.match(r"^\d", ent.text):
        ent._.data["shape"] = "polygonal"

    # All other shapes
    else:
        shape = {}  # Dicts preserve order sets do not
        for token in ent:
            if token._.term == "shape" and token.text != "-":
                word = REPLACE.get(token.lower_, token.lower_)
                shape[word] = 1
        shape = "-".join(shape)
        shape = REPLACE.get(shape, shape)
        ent._.data["shape"] = shape
