from spacy import registry
from traiter.pylib.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns as terms


DECODER = common_patterns.COMMON_PATTERNS | {
    "maybe": {"POS": {"IN": ["PROPN", "NOUN"]}},
    "species": {"ENT_TYPE": "species"},
    "name": {"ENT_TYPE": "lower_taxon"},
    "higher_rank": {"ENT_TYPE": "higher_rank"},
    "higher_taxon": {"ENT_TYPE": "higher_taxon"},
    "subspecies": {"ENT_TYPE": "rank_subspecies"},
    "variety": {"ENT_TYPE": "rank_variety"},
    "subvariety": {"ENT_TYPE": "rank_subvariety"},
    "form": {"ENT_TYPE": "rank_form"},
    "subform": {"ENT_TYPE": "rank_subform"},
}

# ###################################################################################
UPPER_TAXON = MatcherPatterns(
    "taxon.upper",
    on_match="upper_taxon_v1",
    decoder=DECODER,
    patterns=[
        "higher_taxon",
        "higher_rank higher_taxon",
        "higher_rank maybe",
    ],
)


@registry.misc(UPPER_TAXON)
def on_upper_taxon_match(ent):
    ent._.new_label = "taxon"

    for token in ent:

        # Taxon and its rank
        if token._.cached_label == "higher_taxon":
            ent._.data["taxon"] = terms.REPLACE.get(token.lower_, token.text)

            # A given rank overrides the one in the DB
            if not ent._.data.get("higher_rank"):
                ent._.data["rank"] = terms.RANK1.get(token.lower_, "unknown")

        # A given rank trumps the one in the DB
        elif token._.cached_label == "higher_rank":
            ent._.data["rank"] = terms.REPLACE.get(token.lower_, token.lower_)


# ###################################################################################
ON_TAXON_MATCH = "taxon_pattern_v1"

SPECIES_TAXON = MatcherPatterns(
    "taxon.species",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species",
    ],
)

SUBSPECIES_TAXON = MatcherPatterns(
    "taxon.subspecies",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species subspecies? name",
    ],
)

VARIETY_TAXON = MatcherPatterns(
    "taxon.variety",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                  variety name",
        "species subspecies? name variety name",
        "species                  variety maybe",
        "species subspecies? name variety maybe",
    ],
)

SUBVARIETY_TAXON = MatcherPatterns(
    "taxon.subvariety",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                  subvariety name",
        "species variety     name subvariety name",
        "species subspecies? name subvariety name",
        "species                  subvariety maybe",
        "species variety     name subvariety maybe",
        "species subspecies? name subvariety maybe",
    ],
)

FORM_TAXON = MatcherPatterns(
    "taxon.form",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                  form name",
        "species variety     name form name",
        "species subspecies? name form name",
        "species                  form maybe",
        "species variety     name form maybe",
        "species subspecies? name form maybe",
    ],
)

SUBFORM_TAXON = MatcherPatterns(
    "taxon.subform",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                  subform name",
        "species variety     name subform name",
        "species subspecies? name subform name",
        "species                  subform maybe",
        "species variety     name subform maybe",
        "species subspecies? name subform maybe",
    ],
)


@registry.misc(ON_TAXON_MATCH)
def on_taxon_match(ent):
    ent._.new_label = "taxon"
    rank = ent.label_.split(".")[-1]
    for token in ent:
        ...
    parts = [terms.REPLACE(t.lower_, t.text) for t in ent]
    ent._.data["taxon"] = " ".join(parts)
    ent._.data["rank"] = rank
