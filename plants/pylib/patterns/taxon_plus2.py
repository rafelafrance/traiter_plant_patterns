from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from .terms import RANK_ABBREV
from .terms import RANK_TERMS
from .terms import TAXON_TERMS

_LOWER_RANK = """
    subspecies_rank variety_rank subvariety_rank form_rank subform_rank
    """.split()
_LOWER_RANK_SET = set(_LOWER_RANK)

_MAYBE = """ PROPN NOUN """.split()

_DECODER = common.PATTERNS | {
    "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
    "maybe": {"POS": {"IN": _MAYBE}},
    "taxon": {"ENT_TYPE": "taxon"},
    "lower_rank": {"ENT_TYPE": {"IN": _LOWER_RANK}},
    "lower": {"ENT_TYPE": "lower_taxon"},
}


# ###################################################################################
TAXON_PLUS2 = Compiler(
    "taxon_auth",
    on_match="plant_taxon_plus2_v1",
    decoder=_DECODER,
    patterns=[
        "taxon lower_rank lower",
        "taxon lower_rank lower ( auth+                       )",
        "taxon lower_rank lower ( auth+ maybe auth+           )",
        "taxon lower_rank lower ( auth+             and auth+ )",
        "taxon lower_rank lower ( auth+ maybe auth+ and auth+ )",
        "taxon lower_rank lower ( auth+                       ) auth+",
        "taxon lower_rank lower ( auth+ maybe auth+           ) auth+",
        "taxon lower_rank lower ( auth+             and auth+ ) auth+",
        "taxon lower_rank lower ( auth+ maybe auth+ and auth+ ) auth+",
        "taxon lower_rank lower   auth+                        ",
        "taxon lower_rank lower   auth+ maybe auth+            ",
        "taxon lower_rank lower   auth+             and auth+  ",
        "taxon lower_rank lower   auth+ maybe auth+ and auth+  ",
        "taxon lower_rank maybe",
        "taxon lower_rank maybe ( auth+                       )",
        "taxon lower_rank maybe ( auth+ maybe auth+           )",
        "taxon lower_rank maybe ( auth+             and auth+ )",
        "taxon lower_rank maybe ( auth+ maybe auth+ and auth+ )",
        "taxon lower_rank maybe ( auth+                       ) auth+",
        "taxon lower_rank maybe ( auth+ maybe auth+           ) auth+",
        "taxon lower_rank maybe ( auth+             and auth+ ) auth+",
        "taxon lower_rank maybe ( auth+ maybe auth+ and auth+ ) auth+",
        "taxon lower_rank maybe   auth+                        ",
        "taxon lower_rank maybe   auth+ maybe auth+            ",
        "taxon lower_rank maybe   auth+             and auth+  ",
        "taxon lower_rank maybe   auth+ maybe auth+ and auth+  ",
    ],
)


@registry.misc(TAXON_PLUS2.on_match)
def on_taxon_auth_match(ent):
    taxon_ent = next(e for e in ent.ents if e.label_ == "taxon")

    next_is_lower_taxon = False

    taxon_ = [taxon_ent._.data["taxon"]]
    auth = [taxon_ent._.data["authority"]]
    rank = taxon_ent._.data["rank"]

    for token in ent:
        if token.ent_type_ == "taxon":
            continue

        if auth and token.lower_ in common.AND:
            auth.append("and")

        elif token.ent_type_ in _LOWER_RANK:
            taxon_.append(RANK_ABBREV.get(token.lower_, token.lower_))
            rank = RANK_TERMS.replace.get(token.lower_, token.text)
            next_is_lower_taxon = True

        elif next_is_lower_taxon:
            taxon_.append(TAXON_TERMS.replace.get(token.lower_, token.text))
            next_is_lower_taxon = False

        elif token.shape_ in t_const.NAME_SHAPES or token.pos_ in _MAYBE:
            auth.append(token.text)

    ent._.data["taxon"] = " ".join(taxon_)
    ent._.data["rank"] = rank
    ent._.data["authority"] = auth
    ent._.new_label = "taxon"