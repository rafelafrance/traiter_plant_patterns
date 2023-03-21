from spacy import registry
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from . import terms

SIMILAR = """ like similar exactly sympatric affini resembling resembles related
    vicinis vicariant distinguished """.split()


TAXON_LIKE = Compiler(
    "taxon_like",
    on_match="plant_taxon_like_v1",
    decoder=common.PATTERNS
    | {
        "any": {},
        "prep": {"DEP": "prep"},
        "similar": {"LOWER": {"IN": SIMILAR}},
        "taxon": {"ENT_TYPE": {"IN": terms.TAXA}},
    },
    patterns=[
        "similar+ taxon+",
        "similar+ any? prep taxon+",
    ],
)


@registry.misc(TAXON_LIKE.on_match)
def on_taxon_like_match(ent):
    ent._.data = next((e._.data for e in ent.ents if e.label_ in terms.TAXA), {})
    ent._.data["taxon_like"] = ent._.data["taxon"]
    del ent._.data["taxon"]
    relations = [t.text.lower() for t in ent if t.text in SIMILAR]
    ent._.data["relation"] = " ".join(relations)
