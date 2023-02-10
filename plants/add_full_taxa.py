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

Record = namedtuple("Record", "pattern rank replace options")


def main():
    species_id = 220

    args = parse_args()

    id2rank, pattern2rank, rank2id = get_ranks()
    small_ranks = {r for i, r in id2rank.items() if i > species_id}

    taxa = defaultdict(set)

    if args.itis_db:
        get_itis_taxa(taxa, args.itis_db, id2rank, pattern2rank)

    if args.wcvp_file:
        get_wcvp_taxa(taxa, args.wcvp_file, pattern2rank)

    if args.wfot_tsv:
        get_wfot_taxa(taxa, args.wfot_tsv, pattern2rank)

    fix_ranks(taxa)
    taxa = add_missing_species(taxa, small_ranks)

    records = get_records(taxa)
    records = get_binomials(records)
    records = get_trinomials(records, small_ranks)

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
        insert into term_columns
               ( term_set,  extra,    rename)
        values ('taxa',    'extra1', 'rank');
        insert into term_columns
               ( term_set,  extra,    rename)
        values ('taxa',    'extra2', 'options');
        """
    insert = """
        insert into terms
               ( term_set, label,   pattern,  attr,    replace,  extra1,  extra2)
        values ('taxa',   'taxon', :pattern, 'lower', :replace, :extra1, :extra2)
        """
    with sqlite3.connect(const.TAXON_DB) as cxn:
        cxn.executescript(create)
        cxn.executemany(insert, batch)


def get_batch(taxa):
    batch = []
    for rec in tqdm(taxa, desc="batch"):
        batch.append(
            {
                "pattern": rec.pattern.lower(),
                "replace": rec.replace,
                "extra1": rec.rank,
                "extra2": rec.options,
            }
        )
    return batch


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
            elif "phylum" in ranks:
                rank = "phylum"
            elif "suborder" in ranks:
                rank = "suborder"
            else:
                rank = "error"
                print(f"Unhandled multiple rank case: {ranks}", file=sys.stderr)
        taxa[pattern] = rank


def add_missing_species(taxa, small_ranks):
    """Add species that are in trinomials but not in the binomials."""
    new = {}
    for pattern, rank in taxa.items():
        new[pattern] = rank
        if rank in small_ranks:
            words = pattern.split()
            if len(words) < 2:
                continue
            species = " ".join(words[:2])
            new[species] = "species"
    return new


def get_records(taxa):
    return [Record(pattern, rank, pattern, "") for pattern, rank in taxa.items()]


def get_binomials(records):
    """Add an abbreviated binomial for every species."""
    new = []

    all_abbrevs = defaultdict(set)
    for rec in tqdm(records, desc="binomials 1"):
        new.append(rec)

        if rec.rank == "species":
            abbrev = get_abbrev(rec.pattern)
            all_abbrevs[abbrev].add(rec.pattern)

    for abbrev, options in tqdm(all_abbrevs.items(), desc="binomials 2"):
        replace = options.pop() if len(options) == 1 else ""
        options = ",".join(sorted(options)) if len(options) > 1 else ""
        new.append(Record(abbrev, "species", replace, options))

    return new


def get_trinomials(records, small_ranks):
    """Add abbreviated trinomials and remove the subspecies label."""
    subspecies_re = regex.compile(r"\w(spp\.?|subsp\.?|subspecies)\w")

    new = []

    all_abbrevs = defaultdict(set)
    all_ranks = {}

    for rec in tqdm(records, desc="trinomials 1"):
        new.append(rec)

        if rec.rank in small_ranks:
            abbrev = get_abbrev(rec.pattern)
            all_abbrevs[abbrev].add(rec.pattern)
            all_ranks[abbrev] = rec.rank

            trinomial = subspecies_re.sub("", rec.pattern)
            all_abbrevs[trinomial].add(rec.pattern)
            all_ranks[trinomial] = rec.rank

            tri_abbrev = subspecies_re.sub("", abbrev)
            all_abbrevs[tri_abbrev].add(rec.pattern)
            all_ranks[tri_abbrev] = rec.rank

    for abbrev, options in tqdm(all_abbrevs.items(), desc="trinomials 2"):
        rank = all_ranks[abbrev]
        replace = options.pop() if len(options) == 1 else ""
        options = ",".join(sorted(options)) if len(options) > 1 else ""
        new.append(Record(abbrev, rank, replace, options))

    return new


def get_abbrev(pattern):
    genus, *parts = pattern.split()
    abbrev = genus[0].upper() + "."
    abbrev = " ".join([abbrev] + parts)
    return abbrev


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
    itis_kingdom_id = 3

    with sqlite3.connect(itis_db) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = "select complete_name, rank_id from taxonomic_units where kingdom_id = ?"
        rows = [t for t in tqdm(cxn.execute(sql, (itis_kingdom_id,)), desc="itis")]

    for row in rows:
        rank, pattern = id2rank[row["rank_id"]], row["complete_name"]
        add_pattern(taxa, pattern, rank, pattern2rank)


def get_rank(rank, pattern2rank):
    rank = rank.lower()
    return pattern2rank.get(rank, "")


def add_pattern(taxa, pattern, rank, pattern2rank):
    valid_pattern = regex.compile(r"^\p{L}[\p{L}\s'.-]*\p{L}$")
    min_pattern_len = 3
    min_word_len = 2

    rank = rank.lower()
    if not valid_pattern.match(pattern) or len(pattern) < min_pattern_len:
        return
    if any(len(w) < min_word_len for w in pattern.split()):
        return
    if rank not in pattern2rank:
        return
    taxa[pattern].add(rank)


def get_ranks():
    with sqlite3.connect(const.TERM_DB) as cxn:
        cxn.row_factory = sqlite3.Row
        sql = "select * from terms where term_set = 'taxon_ranks'"
        ranks = [t for t in cxn.execute(sql)]
    id2rank = {int(r["extra1"]): r["replace"] for r in ranks}
    rank2id = {r["pattern"]: int(r["extra1"]) for r in ranks}
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
