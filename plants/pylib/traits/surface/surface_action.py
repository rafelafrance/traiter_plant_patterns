from pathlib import Path

from spacy import registry
from traiter.pylib.traits import trait_util

SURFACE_MATCH = "surface_match"

SURFACE_CSV = Path(__file__).parent / "surface_terms.csv"
REPLACE = trait_util.term_data(SURFACE_CSV, "replace")


@registry.misc(SURFACE_MATCH)
def surface_match(ent):
    surface = {}  # Dicts preserve order sets do not
    for token in ent:
        if token._.term == "surface" and token.text != "-":
            word = REPLACE.get(token.lower_, token.lower_)
            surface[word] = 1
    surface = " ".join(surface)
    surface = REPLACE.get(surface, surface)
    ent._.data = {"surface": surface}
