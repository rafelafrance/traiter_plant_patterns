from spacy import registry
from traiter.pylib.matcher_patterns import MatcherPatterns
from traiter.pylib.patterns import common

from ..vocabulary import terms

SIMILAR = """ like similar exactly sympatric affini resembling resembles related
    vicinis vicariant distinguished """.split()


TAXON_LIKE = MatcherPatterns(
    "taxon_like",
    on_match="plant_taxon_like_v1",
    decoder=common.PATTERNS
    | {
        "any": {},
        "prep": {"DEP": "prep"},
        "similar": {"LOWER": {"IN": SIMILAR}},
        "taxon": {"ENT_TYPE": {"IN": terms.TAXON_ENTS}},
    },
    patterns=[
        "similar+ taxon+",
        "similar+ any? prep taxon+",
    ],
    output=["taxon_like"],
)


@registry.misc(TAXON_LIKE.on_match)
def on_taxon_like_match(ent):
    ent._.data = next((e._.data for e in ent.ents if e.label_ in terms.TAXON_ENTS), {})
    ent._.data["taxon_like"] = ent._.data["taxon"]
    del ent._.data["taxon"]
    relations = [t.text.lower() for t in ent if t.text in SIMILAR]
    ent._.data["relation"] = " ".join(relations)
