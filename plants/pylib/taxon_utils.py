import argparse
import csv
import sqlite3
import textwrap
from collections import defaultdict
from pathlib import Path

import regex
from tqdm import tqdm

from . import const


class Ranks:
    def __init__(self):
        self.ranks = self.get_ranks()
        self.id2rank = {int(r["extra1"]): r["replace"] for r in self.ranks}
        self.pattern2rank = {r["pattern"]: r["replace"] for r in self.ranks}
        self.rank2id = {r["pattern"]: int(r["extra1"]) for r in self.ranks}
        self.all_ranks = {r["pattern"] for r in self.ranks}
        self.small_ranks = {
            r for i, r in self.id2rank.items() if i > const.ITIS_SPECIES_ID
        }
        self.big_ranks = {
            r for i, r in self.id2rank.items() if i < const.ITIS_SPECIES_ID
        }
        self.abbrev_list = defaultdict(set)
        for rank in self.ranks:
            self.abbrev_list[rank["replace"]].add(rank["pattern"])

    @staticmethod
    def get_ranks():
        with sqlite3.connect(const.TERM_DB) as cxn:
            cxn.row_factory = sqlite3.Row
            sql = "select * from terms where term_set = 'taxon_ranks'"
            ranks = [t for t in cxn.execute(sql)]
        return ranks

    def has_rank_abbrev(self, rank, pattern):
        return any(w in self.abbrev_list[rank] for w in pattern.split())


def get_raw_taxa(args):
    rank_utils = Ranks()

    taxa = defaultdict(set)

    if args.itis_db:
        get_itis_taxa(taxa, args.itis_db, rank_utils)

    if args.wcvp_file:
        get_wcvp_taxa(taxa, args.wcvp_file, rank_utils)

    if args.wfot_tsv:
        get_wfot_taxa(taxa, args.wfot_tsv, rank_utils)

    return taxa


def get_wfot_taxa(taxa, wfot_tsv, rank_utils):
    with open(wfot_tsv) as in_file:
        reader = csv.DictReader(in_file, delimiter="\t")
        for row in tqdm(reader, desc="wfot"):
            rank = get_rank(row["taxonRank"], rank_utils)
            pattern = row["scientificName"]
            add_pattern(taxa, pattern, rank, rank_utils)


def get_wcvp_taxa(taxa, wcvp_file, rank_utils):
    with open(wcvp_file) as in_file:
        reader = csv.DictReader(in_file, delimiter="|")
        for row in tqdm(reader, desc="wcvp"):
            rank = get_rank(row["taxonrank"], rank_utils)
            pattern = row["scientfiicname"]
            add_pattern(taxa, pattern, rank, rank_utils)


def get_itis_taxa(taxa, itis_db, rank_utils):
    itis_kingdom_id = 3

    with sqlite3.connect(itis_db) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = "select complete_name, rank_id from taxonomic_units where kingdom_id = ?"
        rows = [t for t in tqdm(cxn.execute(sql, (itis_kingdom_id,)), desc="itis")]

    for row in rows:
        rank, pattern = rank_utils.id2rank[row["rank_id"]], row["complete_name"]
        add_pattern(taxa, pattern, rank, rank_utils)


def get_rank(rank, rank_utils):
    rank = rank.lower()
    return rank_utils.pattern2rank.get(rank, "")


def add_pattern(taxa, pattern, rank, rank_utils):
    valid_pattern = regex.compile(r"^\p{L}[\p{L}\s'.-]*\p{L}$")
    min_pattern_len = 3
    min_word_len = 2

    rank = rank.lower()
    if not valid_pattern.match(pattern) or len(pattern) < min_pattern_len:
        return
    if any(len(w) < min_word_len for w in pattern.split()):
        return
    if rank not in rank_utils.pattern2rank:
        return
    taxa[pattern].add(rank)


def get_abbrev(pattern):
    genus, *parts = pattern.split()
    abbrev = genus[0].upper() + "."
    abbrev = " ".join([abbrev] + parts)
    return abbrev


def parse_args():
    description = """Build a database taxon patterns."""
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
