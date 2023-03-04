from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib.pattern_compilers.matcher_compiler import MatcherCompiler
from traiter.pylib.patterns import common_patterns

from . import term_patterns as terms

LOWER_RANK = """
    subspecies_rank variety_rank subvariety_rank form_rank subform_rank
    """.split()
LOWER_RANK_SET = set(LOWER_RANK)

MAYBE = """ PROPN NOUN """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "auth": {"SHAPE": {"IN": t_const.NAME_SHAPES}},
    "maybe": {"POS": {"IN": MAYBE}},
    "taxon": {"ENT_TYPE": "taxon"},
    "lower_rank": {"ENT_TYPE": {"IN": LOWER_RANK}},
    "lower": {"ENT_TYPE": "lower_taxon"},
}


# ###################################################################################
TAXON3 = MatcherCompiler(
    "taxon_auth",
    on_match="plant_taxon3_v1",
    decoder=DECODER,
    patterns=[
        "taxon lower_rank lower",
        "taxon lower_rank lower ( auth+                       )",
        "taxon lower_rank lower ( auth+ maybe auth+           )",
        "taxon lower_rank lower ( auth+             and auth+ )",
        "taxon lower_rank lower ( auth+ maybe auth+ and auth+ )",
        "taxon lower_rank lower   auth+                        ",
        "taxon lower_rank lower   auth+ maybe auth+            ",
        "taxon lower_rank lower   auth+             and auth+  ",
        "taxon lower_rank lower   auth+ maybe auth+ and auth+  ",
        "taxon lower_rank maybe",
        "taxon lower_rank maybe ( auth+                       )",
        "taxon lower_rank maybe ( auth+ maybe auth+           )",
        "taxon lower_rank maybe ( auth+             and auth+ )",
        "taxon lower_rank maybe ( auth+ maybe auth+ and auth+ )",
        "taxon lower_rank maybe   auth+                        ",
        "taxon lower_rank maybe   auth+ maybe auth+            ",
        "taxon lower_rank maybe   auth+             and auth+  ",
        "taxon lower_rank maybe   auth+ maybe auth+ and auth+  ",
    ],
)


@registry.misc(TAXON3.on_match)
def on_taxon_auth_match(ent):
    taxon_ent = next(e for e in ent.ents if e.label_ == "taxon")

    next_is_lower_taxon = False

    taxon = [taxon_ent._.data["taxon"]]
    auth = [taxon_ent._.data["authority"]]
    rank = taxon_ent._.data["rank"]

    for token in ent:
        if token.ent_type_ == "taxon":
            continue

        if auth and token.lower_ in common_patterns.AND:
            auth.append("and")

        elif token.ent_type_ in LOWER_RANK:
            taxon.append(terms.RANK_ABBREV.get(token.lower_, token.lower_))
            rank = terms.REPLACE.get(token.lower_, token.text)
            next_is_lower_taxon = True

        elif next_is_lower_taxon:
            taxon.append(terms.REPLACE.get(token.lower_, token.text))
            next_is_lower_taxon = False

        elif token.shape_ in t_const.NAME_SHAPES or token.pos_ in MAYBE:
            auth.append(token.text)

    ent._.data["taxon"] = " ".join(taxon)
    ent._.data["rank"] = rank
    ent._.data["authority"] = auth
    ent._.new_label = "taxon"
