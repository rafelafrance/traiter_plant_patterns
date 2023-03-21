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

from . import terms

_LOWER_RANK = """
    subspecies_rank variety_rank subvariety_rank form_rank subform_rank
    """.split()
_LOWER_RANKS = set(_LOWER_RANK)

_DECODER = common.PATTERNS | {
    "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
    "taxon": {"ENT_TYPE": "taxon"},
    "_": {"TEXT": {"REGEX": r"^[:._;,]+$"}},
    "monomial": {"ENT_TYPE": "monomial"},
    "lower_rank": {"ENT_TYPE": {"IN": _LOWER_RANK}},
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

    for sub_ent in ent.ents:
        taxa.append(sub_ent._.data["taxon"])
        ent._.data["rank"] = sub_ent._.data["rank"]

    ent._.data["taxon"] = taxa


# ###################################################################################
LOWER_MONOMIAL = Compiler(
    "taxon.lower.monomial",
    on_match="lower_monomial_v1",
    decoder=_DECODER,
    patterns=[
        "lower_rank monomial",
    ],
)


@registry.misc(LOWER_MONOMIAL.on_match)
def on_lower_monomial_match(ent):
    token = next(t for t in ent if t.ent_type_ in _LOWER_RANKS)
    rank = terms.RANK_TERMS.replace.get(token.lower_, token.lower_)

    token = next(t for t in ent if t.ent_type_ == "monomial")
    taxon_ = terms.TAXON_TERMS.replace.get(token.lower_, token.text)

    ent._.data = {"taxon": taxon_, "rank": rank}
    ent._.new_label = "taxon"


# ###################################################################################
TAXON_PLUS1 = Compiler(
    "taxon_auth",
    on_match="plant_taxon_plus1_v1",
    decoder=_DECODER,
    patterns=[
        "taxon ( auth? .? auth? .? auth+           _? )",
        "taxon ( auth? .? auth? .? auth+ and auth+ _? )",
        "taxon   auth? .? auth? .? auth+               ",
        "taxon   auth? .? auth? .? auth+ and auth? .?   auth? .? auth+     ",
        "taxon ( auth? .? auth? .? auth+           _? ) auth? .? auth? .? auth+",
        (
            "taxon ( auth? .? auth? .? auth+ and auth? .? auth? .? auth+ _? )"
            " auth? .? auth? .? auth+"
        ),
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
            if len(token) == 1:
                auth.append(token.text + ".")
            else:
                auth.append(token.text)

    ent._.data["taxon"] = taxon_[0]._.data["taxon"]
    ent._.data["rank"] = taxon_[0]._.data["rank"]
    ent._.data["authority"] = " ".join(auth)
    ent._.new_label = "taxon"
