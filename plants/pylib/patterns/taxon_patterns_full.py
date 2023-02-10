from spacy import registry
from traiter.pylib.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns
from .. import const


DECODER = common_patterns.COMMON_PATTERNS | {
    "auth": {"SHAPE": {"IN": const.NAME_SHAPES}},
    "taxon": {"ENT_TYPE": "taxon"},
}

FULL_TAXON = MatcherPatterns(
    "taxon",
    on_match="plant_taxon_v1",
    decoder=DECODER,
    patterns=[
        "taxon",
    ],
)


@registry.misc(FULL_TAXON.on_match)
def on_full_taxon_match(ent):
    ent._.data["rank"] = term_patterns.FULL_RANK.get(ent.text.lower(), "unknown")
