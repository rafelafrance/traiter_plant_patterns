from spacy import registry
from traiter.pylib.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns as terms
from .. import const


NOT_A_GENUS_PREFIX = """ de el la le no se """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "bad": {"LOWER": {"IN": NOT_A_GENUS_PREFIX}},
    "maybe": {"POS": {"IN": ["PROPN", "NOUN"]}},
    "taxon": {"ENT_TYPE": "taxon"},
}


# ###################################################################################
MULTI_TAXON = MatcherPatterns(
    "multi_taxon",
    on_match="plant_multi_taxon_v1",
    decoder=DECODER,
    patterns=[
        "taxon and taxon",
    ],
)


@registry.misc(MULTI_TAXON.on_match)
def on_multi_taxon_match(ent):
    ent._.data["taxon"] = []
    for token in ent:
        if token._.cached_label == "taxon":
            ent._.data["taxon"].append(terms.REPLACE.get(token.lower_, token.text))
            ent._.data["rank"] = terms.RANK1.get(token.lower_, "unknown")


# ###################################################################################
BAD_TAXON = MatcherPatterns(
    "bad_taxon",
    decoder=DECODER,
    patterns=[
        "bad taxon",
    ],
)


# ###################################################################################
TAXON_AUTH = MatcherPatterns(
    "taxon_auth",
    on_match="taxon_auth_v1",
    decoder=DECODER,
    patterns=[
        "taxon",
        "taxon ( auth+                       )",
        "taxon ( auth+ maybe auth+           )",
        "taxon ( auth+             and auth+ )",
        "taxon ( auth+ maybe auth+ and auth+ )",
        "taxon   auth+                        ",
        "taxon   auth+ maybe auth+            ",
        "taxon   auth+             and auth+  ",
        "taxon   auth+ maybe auth+ and auth+  ",
    ],
)


@registry.misc(TAXON_AUTH.on_match)
def on_full_taxon_match(ent):
    auth = []
    prev_rank = False

    for token in ent:

        # Taxon and its rank
        if token._.cached_label == "taxon":
            ent._.data["taxon"] = terms.REPLACE.get(token.lower_, token.text)

            # A given rank overrides the one in the DB
            if not ent._.data.get("rank"):
                ent._.data["rank"] = terms.RANK1.get(token.lower_, "unknown")

        # A given rank trumps the one in the DB
        elif token._.cached_label == "rank":
            ent._.data["rank"] = terms.REPLACE.get(token.lower_, token.lower_)
            prev_rank = True

        elif token.pos_ in ["PROPN", "NOUN"] and prev_rank:
            ent._.data["taxon"] = terms.REPLACE.get(token.lower_, token.text)
            prev_rank = False

        # Authority
        elif token.pos_ in ["PROPN", "NOUN"] or token.lower_ in common_patterns.AND:
            if token.shape_ in const.TITLE_SHAPES:
                auth.append(token.text)
            elif auth and token.lower_ in common_patterns.AND:
                auth.append(token.text)

    if auth:
        ent._.data["authority"] = " ".join(auth)
