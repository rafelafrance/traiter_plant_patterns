from spacy import registry
from traiter.pylib import actions
from traiter.pylib.pattern_compilers.matcher_compiler import MatcherCompiler
from traiter.pylib.patterns import common_patterns

from . import term_patterns as terms

LOWER_RANK = """
    subspecies_rank variety_rank subvariety_rank form_rank subform_rank
    """.split()
LOWER_RANK_SET = set(LOWER_RANK)

HIGHER_RANK = """
    class_rank division_rank family_rank genus_rank infraclass_rank infradivision_rank
    infrakingdom_rank kingdom_rank order_rank section_rank series_rank subclass_rank
    subdivision_rank subfamily_rank subgenus_rank subkingdom_rank suborder_rank
    subsection_rank subseries_rank subtribe_rank superclass_rank superdivision_rank
    superorder_rank tribe_rank
    """.split()
HIGHER_RANK_SET = {r.removesuffix("_rank") for r in HIGHER_RANK}


ANY_RANK = LOWER_RANK + HIGHER_RANK + ["species_rank"]
ANY_RANK_SET = set(ANY_RANK)

MAYBE = """ PROPN NOUN """.split()

DECODER = common_patterns.COMMON_PATTERNS | {
    "maybe": {"POS": {"IN": MAYBE}},
    "species": {"ENT_TYPE": "binomial"},
    "monomial": {"ENT_TYPE": "monomial"},
    "higher_rank": {"ENT_TYPE": {"IN": HIGHER_RANK}},
    "subspecies": {"ENT_TYPE": "subspecies_rank"},
    "variety": {"ENT_TYPE": "variety_rank"},
    "subvariety": {"ENT_TYPE": "subvariety_rank"},
    "form": {"ENT_TYPE": "form_rank"},
    "subform": {"ENT_TYPE": "subform_rank"},
    "lower_rank": {"ENT_TYPE": {"IN": LOWER_RANK}},
    "species_rank": {"ENT_TYPE": "species_rank"},
}


def is_genus(token):
    return terms.RANKS.get(token.lower_).find("genus") > -1


# ###################################################################################
MONOMIAL = MatcherCompiler(
    "taxon.singleton",
    on_match="single_taxon_v1",
    decoder=DECODER,
    patterns=[
        "monomial",
        "higher_rank  monomial",
        "lower_rank   monomial",
        "species_rank monomial",
    ],
)


@registry.misc(MONOMIAL.on_match)
def on_single_taxon_match(ent):
    rank_from_csv = False
    rank = None
    taxon = None

    for token in ent:
        label = token.ent_type_

        # Taxon and its rank
        if label == "monomial":
            taxon = terms.REPLACE.get(token.lower_, token.text)

            # A given rank will override the one in the DB
            if not rank:
                rank_from_csv = True
                rank = terms.RANKS.get(token.lower_, "unknown")
                rank = rank.split()[0]

        # A given rank overrides the one in the DB
        elif label in ANY_RANK_SET:
            rank_from_csv = False
            rank = terms.REPLACE.get(token.lower_, token.lower_)

        elif token.pos_ in MAYBE:
            taxon = terms.REPLACE.get(token.lower_, token.text)

    if rank_from_csv and rank == "genus":
        raise actions.RejectMatch()

    taxon = taxon.title() if rank in HIGHER_RANK_SET else taxon.lower()

    ent._.data = {"taxon": taxon, "rank": rank}
    ent._.new_label = "taxon"


# ###################################################################################
ON_TAXON_MATCH = "plant_taxon_pattern_v1"

SPECIES_TAXON = MatcherCompiler(
    "taxon.species",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species",
        "monomial monomial",
    ],
)

SUBSPECIES_TAXON = MatcherCompiler(
    "taxon.subspecies",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species            monomial",
        "species subspecies monomial",
        "species subspecies maybe",
    ],
)

VARIETY_TAXON = MatcherCompiler(
    "taxon.variety",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                      variety monomial",
        "species subspecies? monomial variety monomial",
        "species                      variety maybe",
        # "species subspecies? monomial variety maybe",
        # "species subspecies? maybe variety maybe",
    ],
)

SUBVARIETY_TAXON = MatcherCompiler(
    "taxon.subvariety",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                      subvariety monomial",
        "species variety     monomial subvariety monomial",
        "species subspecies? monomial subvariety monomial",
        "species                      subvariety maybe",
        "species variety     monomial subvariety maybe",
        "species subspecies? monomial subvariety maybe",
        "species variety     maybe    subvariety maybe",
        "species subspecies? maybe    subvariety maybe",
        "species variety     maybe    subvariety monomial",
        "species subspecies? maybe    subvariety monomial",
    ],
)

FORM_TAXON = MatcherCompiler(
    "taxon.form",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                      form monomial",
        "species variety     monomial form monomial",
        "species subspecies? monomial form monomial",
        "species                      form maybe",
        "species variety     monomial form maybe",
        "species subspecies? monomial form maybe",
        "species variety     maybe    form maybe",
        "species subspecies? maybe    form maybe",
        "species variety     maybe    form monomial",
        "species subspecies? maybe    form monomial",
    ],
)

SUBFORM_TAXON = MatcherCompiler(
    "taxon.subform",
    on_match=ON_TAXON_MATCH,
    decoder=DECODER,
    patterns=[
        "species                      subform monomial",
        "species variety     monomial subform monomial",
        "species subspecies? monomial subform monomial",
        "species                      subform maybe",
        "species variety     monomial subform maybe",
        "species subspecies? monomial subform maybe",
        "species variety     maybe    subform maybe",
        "species subspecies? maybe    subform maybe",
        "species variety     maybe    subform monomial",
        "species subspecies? maybe    subform monomial",
    ],
)


@registry.misc(ON_TAXON_MATCH)
def on_taxon_match(ent):
    taxon = []
    for i, token in enumerate(ent):
        label = token.ent_type_

        if label == "monomial" and is_genus(token):
            taxon.append(terms.REPLACE.get(token.lower_, token.text))

        elif label == "binomial":
            taxon.append(terms.REPLACE.get(token.lower_, token.text))

        elif label == "monomial" and i != 3:
            taxon.append(terms.REPLACE.get(token.lower_, token.text))

        elif label == "monomial" and i == 3:
            taxon.append(terms.RANK_ABBREV["subspecies"])
            taxon.append(terms.REPLACE.get(token.lower_, token.text))

        elif label in LOWER_RANK_SET:
            taxon.append(terms.RANK_ABBREV.get(token.lower_, token.lower_))

        elif token.pos_ in MAYBE:
            taxon.append(token.text)

        else:
            actions.RejectMatch(f"Bad taxon: {ent.text}")

    taxon = " ".join(taxon)
    taxon = taxon[0].upper() + taxon[1:]

    ent._.data = {"taxon": taxon, "rank": ent.label_.split(".")[-1]}
    ent._.new_label = "taxon"
