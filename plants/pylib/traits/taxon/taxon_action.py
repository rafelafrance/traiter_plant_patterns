import os
import re
from pathlib import Path

from spacy import registry
from traiter.pylib import const as t_const
from traiter.pylib import taxon_util
from traiter.pylib.pipes import reject_match
from traiter.pylib.traits import trait_util

from plants.pylib import const

TAXON_MATCH = "taxon_match"
SINGLE_TAXON_MATCH = "single_taxon_match"
RENAME_TAXON_MATCH = "rename_taxon_match"
MULTI_TAXON_MATCH = "multi_taxon_match"


def get_csvs():
    here = Path(__file__).parent
    csvs = {
        "taxon_terms": here / "taxon_terms.csv",
        "rank_terms": here / "rank_terms.csv",
        "binomial_terms": here / "binomial_terms.zip",
        "monomial_terms": here / "monomial_terms.zip",
    }

    try:
        use_mock_taxa = int(os.getenv("MOCK_TAXA"))
    except (TypeError, ValueError):
        use_mock_taxa = 0

    if (
        not csvs["binomial_terms"].exists()
        or not csvs["monomial_terms"].exists()
        or use_mock_taxa
    ):
        csvs["binomial_terms"] = here / "mock_binomial_terms.csv"
        csvs["monomial_terms"] = here / "mock_monomial_terms.csv"

    return csvs


ALL_CSVS = get_csvs()

LEVEL = trait_util.term_data(ALL_CSVS["rank_terms"], "level")
MONOMIAL_RANKS = trait_util.term_data(ALL_CSVS["monomial_terms"], "ranks")
BINOMIAL_ABBREV = taxon_util.abbrev_binomial_term(ALL_CSVS["binomial_terms"])

RANK_REPLACE = trait_util.term_data(ALL_CSVS["rank_terms"], "replace")
RANK_ABBREV = trait_util.term_data(ALL_CSVS["rank_terms"], "abbrev")
RANK_TERMS = trait_util.read_terms(ALL_CSVS["rank_terms"])
ANY_RANK = sorted({r["label"] for r in RANK_TERMS})
HIGHER_RANK = sorted({r["label"] for r in RANK_TERMS if r["level"] == "higher"})
LOWER_RANK = sorted({r["label"] for r in RANK_TERMS if r["level"] == "lower"})

ABBREV_RE = r"^[A-Z][.,_]$"
AND = ["&", "and", "et"]
MAYBE = """ PROPN NOUN """.split()

TAXON_LABELS = """
    singleton species subspecies variety subvariety form subform
    """.split()

TAXON_LABELS_PLUS = TAXON_LABELS + ["linnaeus", "not_linnaeus", "taxon", "auth1"]


@registry.misc(TAXON_MATCH)
def taxon_match(ent):
    taxon = []
    rank_seen = False

    for i, token in enumerate(ent):
        token._.flag = "taxon"

        if LEVEL.get(token.lower_) == "lower":
            taxon.append(RANK_ABBREV.get(token.lower_, token.lower_))
            rank_seen = True

        elif token._.term == "binomial" and i == 0:
            taxon.append(token.text.title())

        elif token._.term == "binomial" and i > 0:
            taxon.append(token.lower_)

        elif token._.term == "monomial" and i != 2:
            taxon.append(token.lower_)

        elif token._.term == "monomial" and i == 2:
            if not rank_seen:
                taxon.append(RANK_ABBREV["subspecies"])
            taxon.append(token.lower_)

        elif token.pos_ in ["PROPN", "NOUN"]:
            taxon.append(token.text)

        else:
            raise reject_match.RejectMatch()

    if re.match(ABBREV_RE, taxon[0]) and len(taxon) > 1:
        taxon[0] = taxon[0] if taxon[0][-1] == "." else taxon[0] + "."
        abbrev = " ".join(taxon[:2])
        taxon[0] = BINOMIAL_ABBREV.get(abbrev, taxon[0])

    taxon = " ".join(taxon)
    taxon = taxon[0].upper() + taxon[1:]

    ent._.data = {"taxon": taxon, "rank": ent.label_}
    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc(SINGLE_TAXON_MATCH)
def single_taxon_match(ent):
    rank = None
    taxon = None

    for token in ent:
        token._.flag = "taxon"

        # Taxon and its rank
        if token._.term == "monomial":
            taxon = token.lower_
            taxon = taxon.replace("- ", "-")

            # A given rank will override the one in the DB
            rank_ = MONOMIAL_RANKS.get(token.lower_)
            if not rank and rank_:
                rank_ = rank_.split()[0]
                level = LEVEL[rank_]
                if level == "higher" and token.shape_ in t_const.NAME_SHAPES:
                    rank = rank_
                elif (
                    level in ("lower", "species")
                    and token.shape_ not in t_const.TITLE_SHAPES
                ):
                    rank = rank_

        # A given rank overrides the one in the DB
        elif LEVEL.get(token.lower_) in ("higher", "lower"):
            rank = RANK_REPLACE.get(token.lower_, token.lower_)

        elif token.pos_ in ("PROPN", "NOUN"):
            taxon = token.lower_

    if not rank:
        raise reject_match.RejectMatch()

    taxon = taxon.title() if LEVEL[rank] == "higher" else taxon.lower()
    if len(taxon) < const.MIN_TAXON_LEN:
        raise reject_match.RejectMatch()

    ent._.data = {
        "taxon": taxon.title() if LEVEL[rank] == "higher" else taxon.lower(),
        "rank": rank,
    }
    ent[0]._.data = ent._.data
    ent[0]._.flag = "taxon_data"


@registry.misc(MULTI_TAXON_MATCH)
def multi_taxon_match(ent):
    taxa = []

    for sub_ent in ent.ents:
        taxa.append(sub_ent._.data["taxon"])
        ent._.data["rank"] = sub_ent._.data["rank"]

    ent._.data["taxon"] = taxa


@registry.misc(RENAME_TAXON_MATCH)
def rename_taxon_match(ent):
    rank = ""

    for token in ent:

        if token._.flag == "taxon_data":
            ent._.data = token._.data

        elif token._.term in ANY_RANK:
            rank = RANK_REPLACE.get(token.lower_, token.lower_)

    if rank:
        ent._.data["rank"] = rank

    ent._.relabel = "taxon"
