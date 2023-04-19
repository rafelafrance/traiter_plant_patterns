from pathlib import Path

from spacy import registry
from traiter.pylib.traits import trait_util

TAXON_LIKE_MATCH = "taxon_like_match"

TAXON_LIKE_CSV = Path(__file__).parent / "taxon_like_terms.csv"
REPLACE = trait_util.term_data(TAXON_LIKE_CSV, "replace")

TAXON_LABELS = ["taxon", "multi_taxon"]


@registry.misc(TAXON_LIKE_MATCH)
def taxon_like_match(ent):
    ent._.data = next((e._.data for e in ent.ents if e.label_ in TAXON_LABELS), {})
    ent._.data["taxon_like"] = ent._.data["taxon"]
    del ent._.data["taxon"]
    similar = [t.text.lower() for t in ent if t._.term == "similar"]
    ent._.data["relation"] = " ".join(similar)
