from spacy import registry
from traiter.pylib.patterns.matcher_patterns import MatcherPatterns

from . import common_patterns
from . import term_patterns as terms
from .. import const


NOT_A_GENUS_PREFIX = """ de el la le no se costa rica santa """.split()
MAYBE = """ PROPN NOUN """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "auth": {"SHAPE": {"IN": const.NAME_SHAPES}},
    "bad": {"LOWER": {"IN": NOT_A_GENUS_PREFIX}},
    "maybe": {"POS": {"IN": MAYBE}},
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
    taxa = []

    for token in ent:
        if token.ent_type_ == "taxon":
            taxa.append(terms.REPLACE.get(token.lower_, token.text))
            ent._.data["rank"] = terms.RANK1.get(token.lower_, "unknown")

    ent._.data["taxon"] = taxa


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
    on_match="plant_taxon_auth_v1",
    decoder=DECODER,
    patterns=[
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
def on_taxon_auth_match(ent):
    auth = []

    taxon = next(e for e in ent.ents if e.label_ == "taxon")

    for token in ent:
        if token.ent_type_ == "taxon":
            continue

        if auth and token.lower_ in common_patterns.AND:
            auth.append("and")

        elif token.shape_ in const.NAME_SHAPES:
            auth.append(token.text)

        elif token.pos_ in MAYBE:
            auth.append(token.text)

    ent._.data["taxon"] = taxon._.data["taxon"]
    ent._.data["rank"] = taxon._.data["rank"]
    ent._.data["authority"] = " ".join(auth)
    ent._.new_label = "taxon"
