from spacy import registry
from traiter.pylib import actions
from traiter.pylib import term_reader
from traiter.pylib.const import NAME_SHAPES
from traiter.pylib.const import TITLE_SHAPES
from traiter.pylib.pattern_compilers.matcher import Compiler
from traiter.pylib.patterns import common

from . import term as terms
from .. import const

MIN_TAXON_LEN = 3

TAXON_TERMS = term_reader.read(const.TAXA_CSV)
MONOMIAL_TERMS = term_reader.take(TAXON_TERMS, "monomial")
BINOMIAL_TERMS = term_reader.take(TAXON_TERMS, "binomial")
TAXON_REPLACE = term_reader.pattern_dict(TAXON_TERMS, "replace")

RANK_TERMS = term_reader.read(const.VOCAB_DIR / "ranks.csv")
RANK_REPLACE = term_reader.pattern_dict(RANK_TERMS, "ranks")
RANK_ABBREV = term_reader.pattern_dict(RANK_TERMS, "abbrev")

LOWER_RANK = """
    subspecies_rank variety_rank subvariety_rank form_rank subform_rank
    """.split()
LOWER_RANKS = set(LOWER_RANK)

HIGHER_RANK = """
    class_rank division_rank family_rank genus_rank infraclass_rank infradivision_rank
    infrakingdom_rank kingdom_rank order_rank section_rank series_rank subclass_rank
    subdivision_rank subfamily_rank subgenus_rank subkingdom_rank suborder_rank
    subsection_rank subseries_rank subtribe_rank superclass_rank superdivision_rank
    superorder_rank tribe_rank
    """.split()
HIGHER_RANK_NAMES = {r.removesuffix("_rank") for r in HIGHER_RANK}

SPECIES_AND_LOWER = LOWER_RANK + ["species_rank"]

ALL_RANKS = set(SPECIES_AND_LOWER + HIGHER_RANK)

MAYBE = """ PROPN NOUN """.split()

BAD_PREFIX = """ de el la le no se costa santa & """.split()
BAD_SUFFIX = """ river mountain road """.split()

_DECODER = common.PATTERNS | {
    "bad_prefix": {"LOWER": {"IN": BAD_PREFIX}},
    "bad_suffix": {"LOWER": {"IN": BAD_SUFFIX}},
    "maybe": {"POS": {"IN": MAYBE}},
    "binomial": {"ENT_TYPE": "binomial"},
    "monomial": {"ENT_TYPE": "monomial"},
    "higher_rank": {"ENT_TYPE": {"IN": HIGHER_RANK}},
    "subsp.": {"ENT_TYPE": "subspecies_rank"},
    "var.": {"ENT_TYPE": "variety_rank"},
    "subvar.": {"ENT_TYPE": "subvariety_rank"},
    "f.": {"ENT_TYPE": "form_rank"},
    "subf.": {"ENT_TYPE": "subform_rank"},
    "lower_rank": {"ENT_TYPE": {"IN": LOWER_RANK}},
    "species_rank": {"ENT_TYPE": "species_rank"},
}


# ###################################################################################
MONOMIAL = Compiler(
    "taxon.singleton",
    on_match="single_taxon_v1",
    decoder=_DECODER,
    patterns=[
        "monomial",
        "higher_rank  monomial",
        "lower_rank   monomial",
        "species_rank monomial",
    ],
)


@registry.misc(MONOMIAL.on_match)
def on_single_taxon_match(ent):
    # rank_from_csv = False
    rank = None
    taxon = None

    for token in ent:
        label = token.ent_type_

        # Taxon and its rank
        if label == "monomial":
            taxon = terms.REPLACE.get(token.lower_, token.text)

            # A given rank will override the one in the DB
            if not rank:
                rank_ = RANK_REPLACE.get(token.lower_, "unknown")
                rank_ = rank_.split()[0]
                if rank_ in HIGHER_RANK_NAMES and token.shape_ in NAME_SHAPES:
                    # rank_from_csv = True
                    rank = rank_
                elif rank_ in SPECIES_AND_LOWER and token.shape_ not in TITLE_SHAPES:
                    # rank_from_csv = True
                    rank = rank_

        # A given rank overrides the one in the DB
        elif label in ALL_RANKS:
            # rank_from_csv = False
            rank = terms.REPLACE.get(token.lower_, token.lower_)

        elif token.pos_ in MAYBE:
            taxon = terms.REPLACE.get(token.lower_, token.text)

    if not rank:
        raise actions.RejectMatch()

    # if rank_from_csv and rank in GENUS_AND_LOWER:
    #     raise actions.RejectMatch()

    taxon = taxon.title() if rank in HIGHER_RANK_NAMES else taxon.lower()
    if len(taxon) < MIN_TAXON_LEN:
        raise actions.RejectMatch()

    ent._.data = {"taxon": taxon, "rank": rank}
    ent._.new_label = "taxon"


# ###################################################################################
ON_TAXON_MATCH = "plant_taxon_pattern_v1"

SPECIES_TAXON = Compiler(
    "taxon.species",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "binomial",
        "monomial monomial",
    ],
)

SUBSPECIES_TAXON = Compiler(
    "taxon.subspecies",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "binomial        monomial",
        "binomial subsp. monomial",
        "binomial subsp. maybe",
    ],
)

VARIETY_TAXON = Compiler(
    "taxon.variety",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "binomial                  var. monomial",
        "binomial subsp.? monomial var. monomial",
        "binomial                  var. maybe",
        "binomial subsp.? monomial var. maybe",
    ],
)

SUBVARIETY_TAXON = Compiler(
    "taxon.subvariety",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "binomial                  subvar. monomial",
        "binomial var.    monomial subvar. monomial",
        "binomial subsp.? monomial subvar. monomial",
        "binomial                  subvar. maybe",
        "binomial var.    monomial subvar. maybe",
        "binomial subsp.? monomial subvar. maybe",
        "binomial var.    maybe    subvar. maybe",
        "binomial subsp.? maybe    subvar. maybe",
        "binomial var.    maybe    subvar. monomial",
        "binomial subsp.? maybe    subvar. monomial",
    ],
)

FORM_TAXON = Compiler(
    "taxon.form",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "binomial                  f. monomial",
        "binomial var.    monomial f. monomial",
        "binomial subsp.? monomial f. monomial",
        "binomial                  f. maybe",
        "binomial var.    monomial f. maybe",
        "binomial subsp.? monomial f. maybe",
        "binomial var.    maybe    f. maybe",
        "binomial subsp.? maybe    f. maybe",
        "binomial var.    maybe    f. monomial",
        "binomial subsp.? maybe    f. monomial",
    ],
)

SUBFORM_TAXON = Compiler(
    "taxon.subform",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "binomial                  subf. monomial",
        "binomial var.    monomial subf. monomial",
        "binomial subsp.? monomial subf. monomial",
        "binomial                  subf. maybe",
        "binomial var.    monomial subf. maybe",
        "binomial subsp.? monomial subf. maybe",
        "binomial var.    maybe    subf. maybe",
        "binomial subsp.? maybe    subf. maybe",
        "binomial var.    maybe    subf. monomial",
        "binomial subsp.? maybe    subf. monomial",
    ],
)


def is_genus(token):
    return RANK_REPLACE.get(token.lower_).find("genus") > -1


@registry.misc(ON_TAXON_MATCH)
def on_taxon_match(ent):
    taxon = []

    for i, token in enumerate(ent):
        label = token.ent_type_

        if label == "monomial" and is_genus(token):
            taxon.append(RANK_REPLACE.get(token.lower_, token.text))

        elif label == "binomial":
            taxon.append(RANK_REPLACE.get(token.lower_, token.text))

        elif label == "monomial" and i != 3:
            taxon.append(terms.REPLACE.get(token.lower_, token.text))

        elif label == "monomial" and i == 3:
            taxon.append(RANK_ABBREV["subspecies"])
            taxon.append(RANK_REPLACE.get(token.lower_, token.text))

        elif label in LOWER_RANKS:
            taxon.append(RANK_ABBREV.get(token.lower_, token.lower_))

        elif token.pos_ in MAYBE:
            taxon.append(token.text)

        else:
            actions.RejectMatch(f"Bad taxon: {ent.text}")

    taxon = " ".join(taxon)
    taxon = taxon[0].upper() + taxon[1:]

    ent._.data = {"taxon": taxon, "rank": ent.label_.split(".")[-1]}
    ent._.new_label = "taxon"


# ###################################################################################
BAD_TAXON = Compiler(
    "bad_taxon",
    decoder=_DECODER,
    patterns=[
        "bad_prefix monomial",
        "           monomial bad_suffix",
        "bad_prefix monomial bad_suffix",
        "bad_prefix binomial",
        "           binomial bad_suffix",
        "bad_prefix binomial bad_suffix",
    ],
)
