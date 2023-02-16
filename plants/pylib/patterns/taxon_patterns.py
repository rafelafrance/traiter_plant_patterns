from spacy import registry
from traiter.pylib import actions
from traiter.pylib.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns as terms

LOWER_RANK = """
    subspecies_rank variety_rank subvariety_rank form_rank subform_rank
    """.split()
LOWER_RANK_SET = set(LOWER_RANK)

ANY_RANK = LOWER_RANK + """ higher_rank species_rank """.split()
ANY_RANK_SET = set(ANY_RANK)

MAYBE = """ PROPN NOUN """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "maybe": {"POS": {"IN": MAYBE}},
    "species": {"ENT_TYPE": "species_taxon"},
    "lower": {"ENT_TYPE": "lower_taxon"},
    "higher_taxon": {"ENT_TYPE": "higher_taxon"},
    "higher_rank": {"ENT_TYPE": "higher_rank"},
    "subspecies": {"ENT_TYPE": "subspecies_rank"},
    "variety": {"ENT_TYPE": "variety_rank"},
    "subvariety": {"ENT_TYPE": "subvariety_rank"},
    "form": {"ENT_TYPE": "form_rank"},
    "subform": {"ENT_TYPE": "subform_rank"},
    "lower_rank": {"ENT_TYPE": {"IN": LOWER_RANK}},
    "species_rank": {"ENT_TYPE": "species_rank"},
}

# ###################################################################################
HIGHER_TAXON = MatcherPatterns(
    "taxon.singleton",
    on_match="single_taxon_v1",
    decoder=DECODER,
    patterns=[
        "higher_taxon",
        "higher_rank  higher_taxon",
        "lower_rank   lower",
        "species_rank lower",
    ],
)


@registry.misc(HIGHER_TAXON.on_match)
def on_single_taxon_match(ent):
    ent._.new_label = "taxon"
    data = {}
    rank_from_db = False

    for token in ent:

        # Taxon and its rank
        if token._.cached_label in ("higher_taxon", "lower_taxon"):
            data["taxon"] = terms.REPLACE.get(token.lower_, token.text)

            # A given rank will override the one in the DB
            if not data.get("rank"):
                rank_from_db = True
                data["rank"] = terms.RANK1.get(token.lower_, "unknown")

        # A given rank overrides the one in the DB
        elif token._.cached_label in ANY_RANK_SET:
            rank_from_db = False
            data["rank"] = terms.REPLACE.get(token.lower_, token.lower_)

        elif token.pos_ in MAYBE:
            data["taxon"] = terms.REPLACE.get(token.lower_, token.text)

    if rank_from_db and data["rank"] == "genus":
        raise actions.RejectMatch()

    ent._.data = data


# ###################################################################################
ON_TAXON_MATCH = "plant_taxon_pattern_v1"

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
        "species            lower",
        "species subspecies lower",
        "species subspecies maybe",
    ],
)

VARIETY_TAXON = MatcherPatterns(
    "taxon.variety",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                   variety lower",
        "species subspecies? lower variety lower",
        "species                   variety maybe",
        "species subspecies? lower variety maybe",
        "species subspecies? maybe variety maybe",
        "species subspecies? maybe variety lower",
    ],
)

SUBVARIETY_TAXON = MatcherPatterns(
    "taxon.subvariety",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                   subvariety lower",
        "species variety     lower subvariety lower",
        "species subspecies? lower subvariety lower",
        "species                   subvariety maybe",
        "species variety     lower subvariety maybe",
        "species subspecies? lower subvariety maybe",
        "species variety     maybe subvariety maybe",
        "species subspecies? maybe subvariety maybe",
        "species variety     maybe subvariety lower",
        "species subspecies? maybe subvariety lower",
    ],
)

FORM_TAXON = MatcherPatterns(
    "taxon.form",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                   form lower",
        "species variety     lower form lower",
        "species subspecies? lower form lower",
        "species                   form maybe",
        "species variety     lower form maybe",
        "species subspecies? lower form maybe",
        "species variety     maybe form maybe",
        "species subspecies? maybe form maybe",
        "species variety     maybe form lower",
        "species subspecies? maybe form lower",
    ],
)

SUBFORM_TAXON = MatcherPatterns(
    "taxon.subform",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                   subform lower",
        "species variety     lower subform lower",
        "species subspecies? lower subform lower",
        "species                   subform maybe",
        "species variety     lower subform maybe",
        "species subspecies? lower subform maybe",
        "species variety     maybe subform maybe",
        "species subspecies? maybe subform maybe",
        "species variety     maybe subform lower",
        "species subspecies? maybe subform lower",
    ],
)


@registry.misc(ON_TAXON_MATCH)
def on_taxon_match(ent):
    name = []
    for i, token in enumerate(ent):
        label = token._.cached_label

        if label == "species_taxon":
            name.append(terms.REPLACE.get(token.lower_, token.text))

        elif label == "lower_taxon" and i != 3:
            name.append(terms.REPLACE.get(token.lower_, token.text))

        elif label == "lower_taxon" and i == 3:
            name.append(terms.RANK_ABBREV["subspecies"])
            name.append(terms.REPLACE.get(token.lower_, token.text))

        elif label in LOWER_RANK_SET:
            name.append(terms.RANK_ABBREV.get(token.lower_, token.lower_))

        elif token.pos_ in MAYBE:
            name.append(token.text)

        else:
            actions.RejectMatch(f"Bad taxon: {ent.text}")

    ent._.data = {
        "taxon": " ".join(name),
        "rank": ent.label_.split(".")[-1],
    }
    ent._.new_label = "taxon"
