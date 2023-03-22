import regex
from spacy import registry
from traiter.pylib import actions
from traiter.pylib.const import NAME_SHAPES
from traiter.pylib.const import TITLE_SHAPES
from traiter.pylib.pattern_compilers.matcher import Compiler

from . import terms

MIN_TAXON_LEN = 3

_RANKS = terms.TAXON_TERMS.pattern_dict("ranks")

_LOWER_RANK = """
    subspecies_rank variety_rank subvariety_rank form_rank subform_rank
    """.split()
_LOWER_RANKS = set(_LOWER_RANK)

_HIGHER_RANK = """
    class_rank division_rank family_rank genus_rank infraclass_rank infradivision_rank
    infrakingdom_rank kingdom_rank order_rank section_rank series_rank subclass_rank
    subdivision_rank subfamily_rank subgenus_rank subkingdom_rank suborder_rank
    subsection_rank subseries_rank subtribe_rank superclass_rank superdivision_rank
    superorder_rank tribe_rank
    """.split()
_HIGHER_RANK_NAMES = {r.removesuffix("_rank") for r in _HIGHER_RANK}

_SPECIES_AND_LOWER = _LOWER_RANK + ["species_rank"]

_MAYBE = """ PROPN NOUN """.split()

_BAD_PREFIX = """ de el la le no se costa santa & """.split()
_BAD_SUFFIX = """ river mountain road """.split()

_ABBREV_RE = r"^[A-Z][.,_]$"

_DECODER = {
    "A.": {"TEXT": {"REGEX": _ABBREV_RE}},
    "bad_prefix": {"LOWER": {"IN": _BAD_PREFIX}},
    "bad_suffix": {"LOWER": {"IN": _BAD_SUFFIX}},
    "maybe": {"POS": {"IN": _MAYBE}},
    "binomial": {"ENT_TYPE": "binomial"},
    "monomial": {"ENT_TYPE": "monomial"},
    "higher_rank": {"ENT_TYPE": {"IN": _HIGHER_RANK}},
    "subsp": {"ENT_TYPE": "subspecies_rank"},
    "var": {"ENT_TYPE": "variety_rank"},
    "subvar": {"ENT_TYPE": "subvariety_rank"},
    "f.": {"ENT_TYPE": "form_rank"},
    "subf": {"ENT_TYPE": "subform_rank"},
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
        "species_rank monomial",
    ],
)


@registry.misc(MONOMIAL.on_match)
def on_single_taxon_match(ent):
    rank = None
    taxon_ = None

    for token in ent:
        label = token.ent_type_

        # Taxon and its rank
        if label == "monomial":
            taxon_ = terms.TAXON_TERMS.replace.get(token.lower_, token.text)
            taxon_ = taxon_.replace("- ", "-")

            # A given rank will override the one in the DB
            if not rank and (rank_ := terms.TAXON_RANKS.get(taxon_.lower(), "")):
                rank_ = rank_.split()[0]
                if rank_ in _HIGHER_RANK_NAMES and token.shape_ in NAME_SHAPES:
                    rank = rank_
                elif rank_ in _SPECIES_AND_LOWER and token.shape_ not in TITLE_SHAPES:
                    rank = rank_

        # A given rank overrides the one in the DB
        elif label in _HIGHER_RANK:
            rank = terms.RANK_TERMS.replace.get(token.lower_, token.lower_)

        elif token.pos_ in _MAYBE:
            taxon_ = terms.TAXON_TERMS.replace.get(token.lower_, token.text)

    if not rank:
        raise actions.RejectMatch()

    taxon_ = taxon_.title() if rank in _HIGHER_RANK_NAMES else taxon_.lower()
    if len(taxon_) < MIN_TAXON_LEN:
        raise actions.RejectMatch()

    ent._.data = {"taxon": taxon_, "rank": rank}
    ent._.new_label = "taxon"


# ###################################################################################
ON_TAXON_MATCH = "plant_taxon_pattern_v1"

SPECIES_TAXON = Compiler(
    "taxon.species",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=["binomial", "monomial monomial", "A. monomial"],
)

SUBSPECIES_TAXON = Compiler(
    "taxon.subspecies",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "   binomial subsp? monomial",
        "   binomial subsp  maybe",
        "A. monomial subsp? monomial",
        "A. monomial subsp  maybe",
        "A. maybe    subsp? monomial",
        "A. maybe    subsp  maybe",
    ],
)

VARIETY_TAXON = Compiler(
    "taxon.variety",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "   binomial                var monomial",
        "   binomial subsp monomial var monomial",
        "   binomial                var maybe",
        "   binomial subsp monomial var maybe",
        "A. monomial                var monomial",
        "A. monomial subsp monomial var monomial",
        "A. monomial                var maybe",
        "A. monomial subsp monomial var maybe",
        "A. monomial                var monomial",
        "A. monomial subsp monomial var monomial",
        "A. monomial                var maybe",
        "A. monomial subsp monomial var maybe",
        "A. maybe                   var monomial",
        "A. maybe    subsp monomial var monomial",
        "A. maybe                   var maybe",
        "A. maybe    subsp monomial var maybe",
        "A. maybe                   var monomial",
        "A. maybe    subsp monomial var monomial",
        "A. maybe                   var maybe",
        "A. maybe    subsp monomial var maybe",
    ],
)

SUBVARIETY_TAXON = Compiler(
    "taxon.subvariety",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "   binomial                subvar monomial",
        "   binomial var   monomial subvar monomial",
        "   binomial subsp monomial subvar monomial",
        "   binomial                subvar maybe",
        "   binomial var   monomial subvar maybe",
        "   binomial subsp monomial subvar maybe",
        "   binomial var   maybe    subvar maybe",
        "   binomial subsp maybe    subvar maybe",
        "   binomial var   maybe    subvar monomial",
        "   binomial subsp maybe    subvar monomial",
        "A. monomial                subvar monomial",
        "A. monomial var   monomial subvar monomial",
        "A. monomial subsp monomial subvar monomial",
        "A. monomial                subvar maybe",
        "A. monomial var   monomial subvar maybe",
        "A. monomial subsp monomial subvar maybe",
        "A. monomial var   maybe    subvar maybe",
        "A. monomial subsp maybe    subvar maybe",
        "A. monomial var   maybe    subvar monomial",
        "A. monomial subsp maybe    subvar monomial",
        "A. maybe                   subvar monomial",
        "A. maybe    var   monomial subvar monomial",
        "A. maybe    subsp monomial subvar monomial",
        "A. maybe                   subvar maybe",
        "A. maybe    var   monomial subvar maybe",
        "A. maybe    subsp monomial subvar maybe",
        "A. maybe    var   maybe    subvar maybe",
        "A. maybe    subsp maybe    subvar maybe",
        "A. maybe    var   maybe    subvar monomial",
        "A. maybe    subsp maybe    subvar monomial",
    ],
)

FORM_TAXON = Compiler(
    "taxon.form",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "   binomial                f. monomial",
        "   binomial var   monomial f. monomial",
        "   binomial subsp monomial f. monomial",
        "   binomial                f. maybe",
        "   binomial var   monomial f. maybe",
        "   binomial subsp monomial f. maybe",
        "   binomial var   maybe    f. maybe",
        "   binomial subsp maybe    f. maybe",
        "   binomial var   maybe    f. monomial",
        "   binomial subsp maybe    f. monomial",
        "A. monomial                f. monomial",
        "A. monomial var   monomial f. monomial",
        "A. monomial subsp monomial f. monomial",
        "A. monomial                f. maybe",
        "A. monomial var   monomial f. maybe",
        "A. monomial subsp monomial f. maybe",
        "A. monomial var   maybe    f. maybe",
        "A. monomial subsp maybe    f. maybe",
        "A. monomial var   maybe    f. monomial",
        "A. monomial subsp maybe    f. monomial",
        "A. maybe                   f. monomial",
        "A. maybe    var   monomial f. monomial",
        "A. maybe    subsp monomial f. monomial",
        "A. maybe                   f. maybe",
        "A. maybe    var   monomial f. maybe",
        "A. maybe    subsp monomial f. maybe",
        "A. maybe    var   maybe    f. maybe",
        "A. maybe    subsp maybe    f. maybe",
        "A. maybe    var   maybe    f. monomial",
        "A. maybe    subsp maybe    f. monomial",
    ],
)

SUBFORM_TAXON = Compiler(
    "taxon.subform",
    on_match=ON_TAXON_MATCH,
    decoder=_DECODER,
    patterns=[
        "   binomial                subf monomial",
        "   binomial var   monomial subf monomial",
        "   binomial subsp monomial subf monomial",
        "   binomial                subf maybe",
        "   binomial var   monomial subf maybe",
        "   binomial subsp monomial subf maybe",
        "   binomial var   maybe    subf maybe",
        "   binomial subsp maybe    subf maybe",
        "   binomial var   maybe    subf monomial",
        "   binomial subsp maybe    subf monomial",
        "A. monomial                subf monomial",
        "A. monomial var   monomial subf monomial",
        "A. monomial subsp monomial subf monomial",
        "A. monomial                subf maybe",
        "A. monomial var   monomial subf maybe",
        "A. monomial subsp monomial subf maybe",
        "A. monomial var   maybe    subf maybe",
        "A. monomial subsp maybe    subf maybe",
        "A. monomial var   maybe    subf monomial",
        "A. monomial subsp maybe    subf monomial",
        "A. maybe                   subf monomial",
        "A. maybe    var   monomial subf monomial",
        "A. maybe    subsp monomial subf monomial",
        "A. maybe                   subf maybe",
        "A. maybe    var   monomial subf maybe",
        "A. maybe    subsp monomial subf maybe",
        "A. maybe    var   maybe    subf maybe",
        "A. maybe    subsp maybe    subf maybe",
        "A. maybe    var   maybe    subf monomial",
        "A. maybe    subsp maybe    subf monomial",
    ],
)


@registry.misc(ON_TAXON_MATCH)
def on_taxon_match(ent):
    taxon_ = []
    rank_seen = False

    for i, token in enumerate(ent):
        label = token.ent_type_

        if label in _LOWER_RANKS:
            taxon_.append(terms.RANK_ABBREV.get(token.lower_, token.lower_))
            rank_seen = True

        elif label == "binomial":
            taxon_.append(terms.TAXON_TERMS.replace.get(token.lower_, token.text))

        elif label == "monomial" and i != 3:
            taxon_.append(terms.TAXON_TERMS.replace.get(token.lower_, token.text))

        elif label == "monomial" and i == 3:
            if not rank_seen:
                taxon_.append(terms.RANK_ABBREV["subspecies"])
            taxon_.append(terms.RANK_TERMS.replace.get(token.lower_, token.text))

        elif token.pos_ in _MAYBE:
            taxon_.append(token.text)

        else:
            actions.RejectMatch(f"Bad taxon: {ent.text}")

    if regex.match(_ABBREV_RE, taxon_[0]) and len(taxon_) > 1:
        taxon_[0] = taxon_[0] if taxon_[0][-1] == "." else taxon_[0] + "."
        abbrev = " ".join(taxon_[:2])
        if abbrev in terms.BINOMIAL_ABBREVS:
            taxon_[0] = terms.BINOMIAL_ABBREVS[abbrev]

    taxon_ = " ".join(taxon_)
    taxon_ = taxon_[0].upper() + taxon_[1:]

    ent._.data = {"taxon": taxon_, "rank": ent.label_.split(".")[-1]}
    ent._.new_label = "taxon"


# ###################################################################################
BAD_TAXON = Compiler(
    "bad_taxon",
    decoder=_DECODER,
    patterns=[
        "bad_prefix monomial",
        "          monomial bad_suffix",
        "bad_prefix monomial bad_suffix",
        "bad_prefix binomial",
        "          binomial bad_suffix",
        "bad_prefix binomial bad_suffix",
    ],
)
