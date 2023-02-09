#!/usr/bin/env python3
import argparse
import csv
import sqlite3
import textwrap
from collections import defaultdict
from pathlib import Path

import regex
from pylib import const

ITIS_KINGDOM_ID = 3
VALID_PATTERN = regex.compile(r"^[\p{L}×][\p{L}'.-]*\p{L}$")


def main():
    args = parse_args()

    id2rank, pattern2rank, rank2id = get_ranks()

    taxa = defaultdict(set)

    add_old_terms(taxa)

    if args.itis_db:
        add_itis_terms(taxa, args.itis_db, id2rank)

    if args.wcvp_file:
        add_wcvp_terms(taxa, args.wcvp_file, pattern2rank)

    if args.wfot_tsv:
        add_wfot_terms(taxa, args.wfot_tsv, pattern2rank)

    batch = get_batch(taxa, rank2id)

    write_database(batch)


def write_database(batch):
    const.TAXON_DB.unlink()
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
        insert into term_columns
               ( term_set,     extra,    rename)
        values ('plant_taxa', 'extra1', 'rank');
        """
    insert = """
        insert into terms
               ( term_set,     label,         pattern,  attr,   replace, extra1, extra2)
        values ('plant_taxa', 'plant_taxon', :pattern, 'lower', '',     :extra1, '')
        """
    with sqlite3.connect(const.TAXON_DB) as cxn:
        cxn.executescript(create)
        cxn.executemany(insert, batch)


def get_batch(taxa, rank2id):
    batch = []
    for pattern in sorted(taxa.keys()):
        ranks = taxa[pattern]
        ranks = [(r, rank2id[r]) for r in ranks]
        ranks = sorted(ranks, key=lambda r: (r[1], r[0]))
        ranks = " ".join(r[0] for r in ranks)
        batch.append({"pattern": pattern, "extra1": ranks})
    return batch


def add_wfot_terms(taxa, wfot_tsv, pattern2rank):
    with open(wfot_tsv) as in_file:
        reader = csv.DictReader(in_file, delimiter="\t")
        for row in reader:
            if row["taxonRank"].lower() not in pattern2rank:
                continue
            pattern = row["scientificName"].split()[-1].lower()
            rank = pattern2rank[row["taxonRank"].lower()]
            add_pattern(taxa, pattern, rank)


def add_wcvp_terms(taxa, wcvp_file, pattern2rank):
    with open(wcvp_file) as in_file:
        reader = csv.DictReader(in_file, delimiter="|")
        for row in reader:
            if row["taxonrank"].lower() not in pattern2rank:
                continue
            pattern = row["scientfiicname"].split()[-1].lower()
            rank = pattern2rank[row["taxonrank"].lower()]
            add_pattern(taxa, pattern, rank)


def add_itis_terms(taxa, itis_db, id2rank):
    with sqlite3.connect(itis_db) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = "select complete_name, rank_id from taxonomic_units where kingdom_id = ?"
        rows = [t for t in cxn.execute(sql, (ITIS_KINGDOM_ID,))]
        for row in rows:
            pattern = row["complete_name"].split()[-1].lower()
            rank = id2rank[row["rank_id"]]
            add_pattern(taxa, pattern, rank)


def add_pattern(taxa, pattern, rank):
    if VALID_PATTERN.match(pattern):
        taxa[pattern].add(rank)
    else:
        print(f"Rejected pattern: {pattern}")


def add_old_terms(taxa):
    with sqlite3.connect(const.TERM_DB) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = "select pattern, extra1 from terms where term_set = 'plant_taxa'"
        for row in cxn.execute(sql):
            pattern = row["pattern"].lower()
            if VALID_PATTERN.match(pattern):
                taxa[pattern] |= set(row["extra1"].split())
            else:
                print(f"Rejected pattern from old terms: {pattern}")


def get_ranks():
    with sqlite3.connect(const.TERM_DB) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = "select * from terms where term_set = 'taxon_ranks'"
        ranks = [t for t in cxn.execute(sql)]
    id2rank = {r["extra1"]: r["replace"] for r in ranks}
    rank2id = {r["pattern"]: r["extra1"] for r in ranks}
    pattern2rank = {r["pattern"]: r["replace"] for r in ranks}
    return id2rank, pattern2rank, rank2id


def parse_args():
    description = """Add taxon terms to the database."""
    arg_parser = argparse.ArgumentParser(
        description=textwrap.dedent(description), fromfile_prefix_chars="@"
    )

    arg_parser.add_argument(
        "--itis-db",
        type=Path,
        metavar="PATH",
        help="""Get terms from this ITIS database.""",
    )

    arg_parser.add_argument(
        "--wcvp-file",
        type=Path,
        metavar="PATH",
        help="""Get terms from this WCVP file. It is '|' a separated CSV.""",
    )

    arg_parser.add_argument(
        "--wfot-tsv",
        type=Path,
        metavar="PATH",
        help="""Get terms from this WFO Taxonomic TSV.""",
    )

    args = arg_parser.parse_args()
    return args


if __name__ == "__main__":
    main()
