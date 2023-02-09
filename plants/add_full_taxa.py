#!/usr/bin/env python3
import argparse
import csv
import sqlite3
import sys
import textwrap
from collections import defaultdict
from collections import namedtuple
from pathlib import Path

import regex
from pylib import const
from tqdm import tqdm

ITIS_KINGDOM_ID = 3

VALID_PATTERN = regex.compile(r"^\p{L}[\p{L}\s'.-]*\p{L}$")
MIN_PATTERN_LEN = 3
MIN_WORD_LEN = 2

Record = namedtuple("Record", "pattern rank original")


def main():
    args = parse_args()

    id2rank, pattern2rank, rank2id = get_ranks()
    taxa = defaultdict(set)

    if args.itis_db:
        get_itis_taxa(taxa, args.itis_db, id2rank, pattern2rank)

    if args.wcvp_file:
        get_wcvp_taxa(taxa, args.wcvp_file, pattern2rank)

    if args.wfot_tsv:
        get_wfot_taxa(taxa, args.wfot_tsv, pattern2rank)

    records = get_taxa_records(taxa)
    records = get_binomials(records)
    records = get_trinomials(records)

    batch = get_batch(records)
    write_database(batch)


def write_database(batch):
    const.TAXON_DB.unlink(missing_ok=True)
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
    insert = """
        insert into terms
               ( term_set,  label,  pattern,  attr,    replace,  extra1, extra2)
        values ('taxa',    :label, :pattern, 'lower', :replace,  '',     '')
        """
    with sqlite3.connect(const.TAXON_DB) as cxn:
        cxn.executescript(create)
        cxn.executemany(insert, batch)


def get_batch(taxa):
    batch = []
    for pattern, rank, original in tqdm(taxa, desc="batch"):
        batch.append(
            {
                "label": rank,
                "pattern": pattern.lower(),
                "replace": original,
            }
        )
    return batch


def get_taxa_records(taxa):
    records = []
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
            elif "phylum" in ranks:
                rank = "phylum"
            elif "suborder" in ranks:
                rank = "suborder"
            else:
                rank = "error"
                print(f"Unhandled multiple rank case: {ranks}", file=sys.stderr)
        records.append(Record(pattern, rank, pattern))
    return records


def get_trinomials(records):
    new = []
    for pattern, rank, original in tqdm(records, desc="trinomials"):
        if rank != "subspecies":
            new.append(Record(pattern, rank, original))
        else:
            genus, *parts = pattern.split()

            abbrev = genus[0].upper() + "."
            abbrev = " ".join([abbrev] + parts)

            new.append(Record(abbrev, rank, pattern))

            trinomial = regex.sub(r"\w(spp\.?|subsp\.?|subspecies)\w", "", pattern)
            new.append(Record(trinomial, rank, pattern))

            tri_abbrev = regex.sub(r"\w(spp\.?|subsp\.?|subspecies)\w", "", abbrev)
            new.append(Record(tri_abbrev, rank, pattern))
    return new


def get_binomials(records):
    new = []
    for pattern, rank, original in tqdm(records, desc="binomials"):
        if rank != "species":
            new.append(Record(pattern, rank, original))
        else:
            genus, *parts = pattern.split()
            abbrev = genus[0].upper() + "."
            abbrev = " ".join([abbrev] + parts)
            new.append(Record(abbrev, rank, pattern))
    return new


def get_wfot_taxa(taxa, wfot_tsv, pattern2rank):
    with open(wfot_tsv) as in_file:
        reader = csv.DictReader(in_file, delimiter="\t")
        for row in tqdm(reader, desc="wfot"):
            rank = get_rank(row["taxonRank"], pattern2rank)
            pattern = row["scientificName"]
            add_pattern(taxa, pattern, rank, pattern2rank)


def get_wcvp_taxa(taxa, wcvp_file, pattern2rank):
    with open(wcvp_file) as in_file:
        reader = csv.DictReader(in_file, delimiter="|")
        for row in tqdm(reader, desc="wcvp"):
            rank = get_rank(row["taxonrank"], pattern2rank)
            pattern = row["scientfiicname"]
            add_pattern(taxa, pattern, rank, pattern2rank)


def get_itis_taxa(taxa, itis_db, id2rank, pattern2rank):
    with sqlite3.connect(itis_db) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = "select complete_name, rank_id from taxonomic_units where kingdom_id = ?"
        rows = [t for t in tqdm(cxn.execute(sql, (ITIS_KINGDOM_ID,)), desc="itis")]
    for row in rows:
        rank, pattern = id2rank[row["rank_id"]], row["complete_name"]
        add_pattern(taxa, pattern, rank, pattern2rank)


def get_rank(rank, pattern2rank):
    rank = rank.lower()
    return pattern2rank.get(rank, "")


def add_pattern(taxa, pattern, rank, pattern2rank):
    rank = rank.lower()
    if not VALID_PATTERN.match(pattern) or len(pattern) < MIN_PATTERN_LEN:
        return
    if any(len(w) < MIN_WORD_LEN for w in pattern.split()):
        return
    if rank not in pattern2rank:
        return
    taxa[pattern].add(rank)


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
    description = """Build a database for spellchecking taxa from ITIS terms."""
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
