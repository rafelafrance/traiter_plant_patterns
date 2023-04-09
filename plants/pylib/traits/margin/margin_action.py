from pathlib import Path

from spacy import registry
from traiter.pylib.traits import trait_util

MARGIN_MATCH = "margin_custom_pipe"

MARGIN_CSV = Path(__file__).parent / "margin_terms.csv"

REPLACE = trait_util.term_data(MARGIN_CSV, "replace")


@registry.misc(MARGIN_MATCH)
def margin_match(ent):
    margin = {}  # Dicts preserve order sets do not
    for token in ent:
        if token._.term in ["margin", "shape"] and token.text != "-":
            word = REPLACE.get(token.lower_, token.lower_)
            margin[word] = 1
    margin = "-".join(margin.keys())
    margin = REPLACE.get(margin, margin)
    ent._.data["margin"] = margin
