#!/usr/bin/env python3
"""We use full species names but only single taxon names for higher and lower ranks."""
import sqlite3
import sys
from collections import defaultdict
from collections import namedtuple

from pylib import const
from pylib import taxon_utils
from tqdm import tqdm
from traiter.pylib import log

Record = namedtuple("Record", "term_set label pattern attr replace extra1 extra2")


def main():
    log.started()
    args = taxon_utils.parse_args()

    rank_utils = taxon_utils.Ranks()

    taxa = taxon_utils.get_raw_taxa(args)

    fix_ranks(taxa)

    taxa = fix_species(taxa, rank_utils)
    taxa = add_missing_species(taxa, rank_utils)

    remove_problem_taxa(taxa)

    species = get_species(taxa)
    higher_taxa = get_higher_taxa(taxa, rank_utils)
    lower_taxa = get_lower_taxa(taxa, rank_utils)

    create_tables()
    insert_ranks()

    batch = species + higher_taxa + lower_taxa
    write_database(batch)

    log.finished()


def write_database(batch):
    insert = """
        insert into terms
               ( term_set,  label,  pattern,  attr,  replace,  extra1,  extra2)
        values (:term_set, :label, :pattern, :attr, :replace, :extra1, :extra2)
        """
    with sqlite3.connect(const.FULL_TAXON_DB) as cxn:
        cxn.executemany(insert, batch)


def create_tables():
    const.FULL_TAXON_DB.unlink(missing_ok=True)
    create = """
        create table terms (
            term_set text,
            label    text,
            pattern  text,
            attr     text,
            replace  text,
            extra1   blob,
            extra2   blob
        );
        create table term_columns (
            term_set text,
            extra    text,
            rename   text
        );
        """
    with sqlite3.connect(const.FULL_TAXON_DB) as cxn:
        cxn.executescript(create)


def insert_ranks():
    with sqlite3.connect(const.FULL_TAXON_DB) as cxn:
        cxn.execute(f"attach database '{const.TERM_DB}' as aux")
        sql = """
            insert into term_columns
            select * from aux.term_columns where term_set in ('taxa', 'ranks')"""
        cxn.execute(sql)
        sql = "insert into terms select * from aux.terms where term_set = 'ranks'"
        cxn.execute(sql)


def get_higher_taxa(taxa, rank_utils):
    bad_taxa = ("Temp", "Uncertain")
    records = []
    for taxon, rank in tqdm(taxa.items(), desc="higher"):
        if rank in rank_utils.big_ranks:
            words = taxon.split()
            if words[0] not in bad_taxa:
                word = words[-1]
                records.append(
                    Record(
                        term_set="taxa",
                        label="higher_taxon",
                        pattern=word.lower(),
                        attr="lower",
                        replace=word.title(),
                        extra1=rank,
                        extra2="",
                    )
                )
    return records


def get_lower_taxa(taxa, rank_utils):
    lower = defaultdict(set)

    all_ranks = rank_utils.all_ranks
    small_ranks = rank_utils.small_ranks.copy()
    # ranks.add("species")

    for taxon, rank in tqdm(taxa.items(), desc="lower 1"):
        if rank in small_ranks:
            for word in taxon.split():
                if word[0].lower() == word[0] and word.lower() not in all_ranks:
                    lower[word].add(rank)

    records = []
    for taxon, ranks in tqdm(lower.items(), desc="lower 2"):
        records.append(
            Record(
                term_set="taxa",
                label="lower_taxon",
                pattern=taxon.lower(),
                attr="text",
                replace="",
                extra1=" ".join(ranks),
                extra2="",
            )
        )
    return records


def get_species(taxa):
    species = []
    all_abbrevs = defaultdict(set)

    for taxon, rank in tqdm(taxa.items(), desc="species 1"):
        if rank == "species":
            species.append(
                Record(
                    term_set="taxa",
                    label="species_taxon",
                    pattern=taxon.lower(),
                    attr="lower",
                    replace=taxon,
                    extra1=rank,
                    extra2="",
                )
            )
            abbrev = taxon_utils.get_abbrev(taxon)
            all_abbrevs[abbrev].add(taxon)

    for abbrev, options in tqdm(all_abbrevs.items(), desc="species 2"):
        replace = options.pop() if len(options) == 1 else ""
        options = ",".join(sorted(options)) if len(options) > 1 else ""
        species.append(
            Record(
                term_set="taxa",
                label="species_taxon",
                pattern=abbrev.lower(),
                attr="lower",
                replace=replace,
                extra1="species",
                extra2=options,
            )
        )

    return species


def fix_ranks(taxa):
    """Choose only one rank per taxon."""
    for pattern, ranks in taxa.items():
        if len(ranks) == 1:
            rank = ranks.pop()
        else:
            word_count = len(pattern.split())
            if "species" in ranks and "variety" in ranks and word_count == 2:
                rank = "species"
            elif "species" in ranks and "variety" in ranks and word_count > 2:
                rank = "variety"
            elif "family" in ranks:
                rank = "family"
            elif "division" in ranks:
                rank = "division"
            elif "suborder" in ranks:
                rank = "suborder"
            else:
                rank = "error"
                print(f"Unhandled multiple rank case: {ranks}", file=sys.stderr)
        taxa[pattern] = rank


def fix_species(taxa, rank_utils):
    new = {}
    for pattern, rank in taxa.items():
        if rank != "species":
            new[pattern] = rank
        else:
            wc = len(pattern.split())
            if wc < 2:
                pass
            elif wc == 2:
                new[pattern] = rank
            elif wc > 2 and rank_utils.has_rank_abbrev("section", pattern):
                pass
            elif wc > 2 and rank_utils.has_rank_abbrev("variety", pattern):
                new[pattern] = "variety"
            elif wc > 2 and rank_utils.has_rank_abbrev("form", pattern):
                new[pattern] = "form"
            elif wc == 3:
                new[pattern] = "subspecies"
    return new


def add_missing_species(taxa, rank_utils):
    """Add species that are in trinomials but not in the binomials."""
    new = {}
    for pattern, rank in taxa.items():
        new[pattern] = rank
        if rank in rank_utils.small_ranks:
            words = pattern.split()
            if len(words) < 2:
                continue
            species = " ".join(words[:2])
            new[species] = "species"
    return new


def remove_problem_taxa(taxa):
    """Some upper taxa interfere with other parses."""
    problem_taxa = """ Side """.split()
    for problem in problem_taxa:
        del taxa[problem]


if __name__ == "__main__":
    main()
