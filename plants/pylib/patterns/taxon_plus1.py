"""Get taxon patterns that are build up from previous taxon notations:

a) A taxon with an authority like: "Canis lupus Linnaeus".
   The authority is Linnaeus.
b) Multiple taxa like: "Mimosa sensitiva and Canis lupus".

Use the n parameter to build up taxa with authorities at multiple ranks.

1 if your taxa have at maximum one citation per taxon like:
    "Canis lupus Linnaeus"
    "Linnaeus" is the single authority.

2 if you may have 2 citations per taxon like:
    "Vicia villosa Roth ssp. varia (Khan)"
    The species authority is "Roth" and the subspecies authority is "Khan".
    The taxon rank is subspecies.

3 if you have up to 3 citations in a taxon like:
    "Mimosa gracilis Barneby subsp. capillipes Khan var. brevissima (Bozo)"
    Three authorities: Barneby, Khan, and Bozo. The rank here is variant.
"""
from spacy import registry
from traiter.pylib import actions
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from .terms import TAXON_RANKS
from .terms import TAXON_TERMS


_DECODER = common.PATTERNS | {
    "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
    "taxon": {"ENT_TYPE": "taxon"},
    "_": {"TEXT": {"REGEX": r"^[:._;,]+$"}},
}


# ###################################################################################
MULTI_TAXON = Compiler(
    "multi_taxon",
    on_match="plant_multi_taxon_v1",
    decoder=_DECODER,
    patterns=[
        "taxon and taxon",
    ],
)


@registry.misc(MULTI_TAXON.on_match)
def on_multi_taxon_match(ent):
    taxa = []

    for token in ent:
        if token.ent_type_ == "taxon":
            taxa.append(TAXON_TERMS.replace.get(token.lower_, token.text))
            ent._.data["rank"] = TAXON_RANKS.replace.get(token.lower_, "unknown")

    ent._.data["taxon"] = taxa


# ###################################################################################
TAXON_PLUS1 = Compiler(
    "taxon_auth",
    on_match="plant_taxon_plus1_v1",
    decoder=_DECODER,
    patterns=[
        "taxon ( auth+           _? )",
        "taxon ( auth+ and auth+ _? )",
        "taxon   auth+               ",
        "taxon   auth+ and auth+     ",
        "taxon ( auth+           _? ) auth+",
        "taxon ( auth+ and auth+ _? ) auth+",
    ],
)


@registry.misc(TAXON_PLUS1.on_match)
def on_taxon_auth_match(ent):
    auth = []

    taxon_ = [e for e in ent.ents if e.label_ == "taxon"]
    if len(taxon_) != 1:
        raise actions.RejectMatch()

    for token in ent:
        if token.ent_type_ == "taxon":
            continue

        if auth and token.lower_ in common.AND:
            auth.append("and")

        elif token.shape_ in t_const.NAME_SHAPES:
            auth.append(token.text)

    ent._.data["taxon"] = taxon_[0]._.data["taxon"]
    ent._.data["rank"] = taxon_[0]._.data["rank"]
    ent._.data["authority"] = " ".join(auth)
    ent._.new_label = "taxon"
