from spacy import registry
from traiter.pylib import actions
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from . import term as terms


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
            taxa.append(terms.REPLACE.get(token.lower_, token.text))
            ent._.data["rank"] = terms.RANKS.get(token.lower_, "unknown")

    ent._.data["taxon"] = taxa


# ###################################################################################
TAXON_PLUS1 = Compiler(
    "taxon_auth",
    on_match="plant_taxon2_v1",
    decoder=_DECODER,
    patterns=[
        "taxon ( auth+           _? )",
        "taxon ( auth+ and auth+ _? )",
        "taxon   auth+               ",
        "taxon   auth+ and auth+     ",
    ],
)


@registry.misc(TAXON_PLUS1.on_match)
def on_taxon_auth_match(ent):
    auth = []

    taxon = [e for e in ent.ents if e.label_ == "taxon"]
    if len(taxon) != 1:
        raise actions.RejectMatch()

    for token in ent:
        if token.ent_type_ == "taxon":
            continue

        if auth and token.lower_ in common.AND:
            auth.append("and")

        elif token.shape_ in t_const.NAME_SHAPES:
            auth.append(token.text)

    ent._.data["taxon"] = taxon[0]._.data["taxon"]
    ent._.data["rank"] = taxon[0]._.data["rank"]
    ent._.data["authority"] = " ".join(auth)
    ent._.new_label = "taxon"
